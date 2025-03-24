import pytest
import responses

from tests.mocks import MockCache, MockConfig


@pytest.fixture(scope="function")
def mock_gh_thisuser():
    responses.add(
        responses.GET,
        f"https://api.github.com/user",
        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer sometoken"},
        status=200,
        json= {"id": 10, "login": "myuser"},
    )

@pytest.fixture(scope="function")
def mock_gh_thisuser_wrongtoken():
    responses.add(
        responses.GET,
        f"https://api.github.com/user",
        status=401,
    )

@pytest.fixture(scope="function")
def mock_gh_repo_gazers():
    responses.add(
        responses.GET,
        f"https://api.github.com/repos/myuser/myrepo/stargazers?per_page=100",
        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer sometoken"},
        status=200,
        json=[
            {"id": 1, "login": "user_1"},
            {"id": 2, "login": "user_2"},
            {"id": 3, "login": "user_3"},
        ],
    )

@pytest.fixture(scope="function")
def mock_gh_gazers_repos_user1():
    responses.add(
        responses.GET,
        f"https://api.github.com/users/user_1/starred?per_page=100",
        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer sometoken"},
        status=200,
        json=[
            {"id": 1, "full_name": "repo_1"},
            {"id": 2, "full_name": "repo_2"},
        ],
    )

@pytest.fixture(scope="function")
def mock_gh_gazers_repos_user2():
    responses.add(
        responses.GET,
        f"https://api.github.com/users/user_2/starred?per_page=100",
        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer sometoken"},
        status=200,
        json=[
            {"id": 2, "full_name": "repo_2"},
            {"id": 3, "full_name": "repo_3"},
        ],
    )

@pytest.fixture(scope="function")
def mock_gh_gazers_repos_user3():
    responses.add(
        responses.GET,
        f"https://api.github.com/users/user_3/starred?per_page=100",
        headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer sometoken"},
        status=200,
        json=[
            {"id": 2, "full_name": "repo_2"},
            {"id": 3, "full_name": "repo_3"},
            {"id": 4, "full_name": "repo_4"},
            {"id": 5, "full_name": "repo_5"},
        ],
    )

@pytest.mark.usefixtures("mock_gh_thisuser", "mock_gh_repo_gazers", "mock_gh_gazers_repos_user1", "mock_gh_gazers_repos_user2", "mock_gh_gazers_repos_user3")
@responses.activate
def test_starneighbours(client, auth_headers, mocker):
    mocker.patch("starneighbours.app.starneighbours.cache", MockCache())
    response = client.get(f"/repos/myuser/myrepo/starneighbours", headers=auth_headers)
    assert response.status_code == 200

    resp_data = response.json()
    resp_data.sort(key=lambda x: x["repo"])
    assert resp_data == [
        {"repo": "repo_1", "stargazers": ["user_1"]},
        {"repo": "repo_2", "stargazers": ["user_1", "user_2", "user_3"]},
        {"repo": "repo_3", "stargazers": ["user_2", "user_3"]},
        {"repo": "repo_4", "stargazers": ["user_3"]},
        {"repo": "repo_5", "stargazers": ["user_3"]},
    ]

@pytest.mark.usefixtures("mock_gh_thisuser_wrongtoken")
@responses.activate
def test_token_error(client, mocker):
    mocker.patch("starneighbours.settings.settings", MockConfig())
    wrong_auth_headers = {"Authorization": f"Bearer wrong"}
    response = client.get(f"/repos/myuser/myrepo/starneighbours", headers=wrong_auth_headers)
    assert response.status_code == 401

    resp_data = response.json()
    assert resp_data["detail"] == "401: Unauthorized, token authenticaton failed"
