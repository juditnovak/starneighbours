import json

import pytest
import responses

from starneighbours.settings import settings

from .mocks import MockConfig


@pytest.fixture(scope="session")
def mock_gh_code_callback():
    responses.add(
        responses.POST,
        "https://github.com/login/oauth/access_token",
        status=200,
        json={"access_token": "token"}
    )


@pytest.fixture(scope="session")
def mock_gh_code_callback_unauthorized():
    responses.add(
        responses.POST,
        "https://github.com/login/oauth/access_token",
        status=401,
    )

@pytest.fixture(scope="session")
def mock_gh_code_callback_missing_token():
    responses.add(
        responses.POST,
        "https://github.com/login/oauth/access_token",
        status=200,
    )


@pytest.mark.usefixtures("mock_gh_code_callback")
@responses.activate
def test_auth_ok(client, mocker):

    mocker.patch("starneighbours.app.auth.settings", MockConfig())

    data = {
        "code": "someGHcode",
        "client_id": settings.app_client_id,
        "client_secret": settings.app_client_secret,
    }
    response = client.get("/token", params=data)
    assert response.status_code == 200

    resp_data = response.json()
    assert resp_data["access_token"] is not None
    assert resp_data["token_type"] == "bearer"


@pytest.mark.usefixtures("mock_gh_code_callback")
@responses.activate
def test_auth_no_credentials(client):

    data = {
        "code": "someGHcode",
        "client_id": settings.app_client_id,
        "client_secret": settings.app_client_secret,
    }
    response = client.get("/token", params=data)
    assert response.status_code == 401


@pytest.mark.usefixtures("mock_gh_code_callback_unauthorized")
@responses.activate
def test_auth_no_credentials(client):

    data = {
        "code": "someGHcode",
        "client_id": settings.app_client_id,
        "client_secret": settings.app_client_secret,
    }
    response = client.get("/token", params=data)
    assert response.status_code == 401


@pytest.mark.usefixtures("mock_gh_code_callback_unauthorized")
@responses.activate
def test_auth_no_credentials(client):

    data = {
        "code": "someGHcode",
        "client_id": settings.app_client_id,
        "client_secret": settings.app_client_secret,
    }
    response = client.get("/token", params=data)
    assert response.status_code == 401


@pytest.mark.usefixtures("mock_gh_code_callback_missing_token")
@responses.activate
def test_auth_token_missing(client):

    data = {
        "code": "someGHcode",
        "client_id": settings.app_client_id,
        "client_secret": settings.app_client_secret,
    }
    response = client.get("/token", params=data)
    assert response.status_code == 401
