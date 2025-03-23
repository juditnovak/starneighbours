import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles

from starneighbours.routers.auth_router import auth_router
from starneighbours.routers.stars_router import stars_router
from starneighbours.settings import settings

logging.basicConfig()
logging.getLogger().setLevel(settings.log_level)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FastAPI application",
        version="1.0.0",
        description="JWT Authentication and Authorization",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_app():
    app = FastAPI(swagger_ui_parameters={})
    app.include_router(stars_router)
    app.include_router(auth_router)

    app.mount("/static", StaticFiles(directory="./static"), name="static")

    return app


app = create_app()

app.openapi = custom_openapi
