from pydantic import BaseModel


class StarNeighbour(BaseModel):
    repo: str
    stargazers: list[str]
