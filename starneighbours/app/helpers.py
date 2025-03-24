import logging
from typing import Any, Generator

import requests
from fastapi import HTTPException

from starneighbours.settings import auth_on

logger = logging.getLogger(__name__)


def generate_headers(token: str) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json"}
    if auth_on():
        headers.update({"Authorization": f"{token}"})
    return headers


def query_list(token: str, url: str) -> Generator[dict, None, None]:
    """Processing GET requests page-by-page."""
    next_page = url
    params = {"per_page": 100}
    while next_page:
        resp = requests.get(next_page, headers=generate_headers(token), params=params)
        logger.debug("Feching URL %s", url)

        next_page = resp.links.get("next", {}).get("url")
        params = {}

        if resp.status_code != 200:
            raise HTTPException(
                status_code=resp.status_code, detail="Error when querying {url}"
            )
        for item in resp.json():
            yield item


def query_item(token: str, url: str) -> dict[str, Any]:
    """Process GET request for queries when a single item is returned."""
    resp = requests.get(url, headers=generate_headers(token))

    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code)
    return resp.json()
