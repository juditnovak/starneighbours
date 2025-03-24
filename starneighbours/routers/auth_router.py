from fastapi import APIRouter, HTTPException

from starneighbours.app.auth import (
    AuthMissingCredentials,
    AuthMissingToken,
    get_gh_user_token,
)
from starneighbours.routers.validators.auth_validator import Token

auth_router = APIRouter()


@auth_router.get("/token")
async def token(code: str) -> Token:
    try:
        token_str = get_gh_user_token(code)
    except AuthMissingCredentials:
        raise HTTPException(status_code=401, detail="Missing application credentials")
    except AuthMissingToken:
        raise HTTPException(status_code=401, detail="Token was not received")
    return Token(access_token=token_str, token_type="bearer")
