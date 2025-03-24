from typing import Annotated

from fastapi import APIRouter, Header, HTTPException

from starneighbours.app.helpers import query_item
from starneighbours.app.starneighbours import get_gazers_of_repo
from starneighbours.routers.validators.stars_validator import StarNeighbour
from starneighbours.settings import auth_on

stars_router = APIRouter(
    prefix="/repos",
    tags=["starneighbours"],
    responses={404: {"description": "stars not found"}},
)


@stars_router.get("/{owner}/{repo}/starneighbours")
def endpoint_starneighbours(
    owner: str,
    repo: str,
    authorization: Annotated[str, Header()] = "",
) -> list[StarNeighbour]:
    # Checking if token is provided when in authenticated mode
    if auth_on() and not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    # Checking token validity, if needed
    if auth_on() and authorization:
        try:
            query_item(authorization, "https://api.github.com/user")
        except HTTPException as err:
            raise HTTPException(
                status_code=err.status_code,
                detail=f"{str(err)}, token authenticaton failed",
            )
    return get_gazers_of_repo(authorization, owner.strip(), repo.strip())
