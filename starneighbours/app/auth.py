import logging

import requests
from passlib.context import CryptContext

from starneighbours.exceptions import StarNeighboursError
from starneighbours.settings import settings

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthMissingCredentials(StarNeighboursError):
    msg = "Wrong user credentials"


class AuthMissingToken(StarNeighboursError):
    msg = "No token"


def get_gh_user_token(code: str) -> str:
    if not settings.app_client_id or not settings.app_client_secret:
        raise AuthMissingCredentials

    resp = requests.post(
        "https://github.com/login/oauth/access_token",
        json={
            "client_id": settings.app_client_id,
            "client_secret": settings.app_client_secret,
            "code": code,
        },
        headers={"Accept": "application/json", "Content-Type": "application/json"},
    )

    if resp.status_code == 200:
        token = resp.json().get("access_token")
        if token:
            return token
    raise AuthMissingToken
