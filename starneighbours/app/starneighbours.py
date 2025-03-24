import logging
from typing import Generator, Iterable

from redis import StrictRedis

from starneighbours.app.helpers import query_list
from starneighbours.exceptions import StarNeighboursError
from starneighbours.routers.validators.stars_validator import StarNeighbour
from starneighbours.settings import settings

logger = logging.getLogger(__name__)


cache = StrictRedis(decode_responses=True, host=settings.cache_server)

CACHE_USER_PREFIX = "USER"
CACHE_REPO_PREFIX = "REPO"


class GazerNotFound(StarNeighboursError):
    msg = "Gazer not found."


class RepoNotFound(StarNeighboursError):
    msg = "Gazer not found."


def encode_list(input: list[str]) -> str:
    return ":".join(input)


def decode_list(input: str) -> list[str]:
    return input.split(":")


def repo_cache_key(repo: str) -> str:
    return f"{CACHE_REPO_PREFIX}_{repo}"


def gazer_cache_key(gazer: str) -> str:
    return f"{CACHE_USER_PREFIX}_{gazer}"


def cache_set(key: str, value: str):
    cache.set(key, value)
    cache.expire(key, settings.cache_ttl)
    logger.debug("Caching %s: %s", key, value)


def cache_get(key: str) -> list[str]:
    retval = decode_list(str(cache.get(key)))
    logger.debug("Found in cache %s", retval)
    return retval


def process_gazers_of_repo(
    token: str, user: str, repo: str
) -> Generator[str, None, None]:
    """Processing gazers for a repository."""
    for gazer in query_list(
        token, f"https://api.github.com/repos/{user}/{repo}/stargazers"
    ):
        yield gazer.get("login", "")


def get_gazers_of_repo(token: str, user: str, repo: str) -> list[StarNeighbour]:
    """Core functionality: iterating through all starred repos of all gazers of the repo in quesiton.

    Cache is used to store essential data.
    """
    calc = {}
    retval = []
    all_repos: set[str] = set()
    all_gazers = []
    gazer_query: Iterable[str]

    repo_cached = cache.exists(repo_cache_key(repo))
    if repo_cached:
        gazer_query = cache_get(repo_cache_key(repo))
    else:
        gazer_query = process_gazers_of_repo(token, user, repo)

    for gazer in gazer_query:
        if not gazer:
            continue

        gazer_cached = cache.exists(gazer_cache_key(gazer))
        if gazer_cached:
            calc[gazer] = cache_get(gazer_cache_key(gazer))
        else:
            query_url = f"https://api.github.com/users/{gazer}/starred"
            calc[gazer] = [repo["full_name"] for repo in query_list(token, query_url)]

        all_repos = all_repos | set(calc[gazer])
        cache_set(gazer_cache_key(gazer), encode_list(calc[gazer]))

        all_gazers.append(gazer)

    if not repo_cached:
        cache_set(repo_cache_key(repo), encode_list(all_gazers))

    for repo in all_repos:
        rg = {"repo": repo, "stargazers": []}
        for gazername in calc:
            if repo in calc[gazername]:
                rg["stargazers"].append(gazername)  # type: ignore [attr-defined]

        retval.append(StarNeighbour(**rg))  # type: ignore [arg-type]

    return retval
