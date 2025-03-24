# StarNeighbours 

A web API following the concept of "neighbouring" repositories based on users who starred them.


## Details

A neighbour of a repository A as a repository B that has been starred by a same user.

> For example, if `joe` adds a star to the repository `projectA` and `projectB`, we define those repositories `projectA` and `projectB` as being *neighbours*.
>

## Installation

Simplest is to use Docker, that way

```
docker compose up
```
should do it all.

Alternatively you need a functional Redis service, and to define the `REDIS_HOST` environment variable to point to the server.

Then from the repository run 
```
uv run fastapi dev starneighbours/main.py
```

## Usage

### No authentication

The application works out of the box benefiting from public access to GitHub REST API.


### Authentication

In case higher access rate is preferred, the application should be run in authenticated mode.

#### 1. GitHub App
This requires additional setup, as a [GitHub Oauth App](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/creating-an-oauth-app)
needs to be set up ensuring credentials for the application. 
The Authorization callback URL of the GitHub App has to point to the `<APP_BASE_URL>/token` endpoint.

#### 2. Local settings
GitHub App credentials have to be communicated to the
application as `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` environment variables.

#### 3. Obtaining Oauth token
A static HTML page is available at `<APP_BASE_URL>/static/login.html`. It will redirect to GitHub requesting permission
from the user, if s/he would authorize this GitHub App to authenticate in his/her behalf. 
(The application is not requesting any scopes, but uses the default i.e. "public access" Oauth App 
authorization scope. See [Scopes for Oauth apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps))

#### 4. Try it out!
Once the application is up and running, the OpenAPI documentation interface should come up on
```
<APP_BASE_URL>/docs
```
which can be handy for manual tests.

Here we can log in using the **Authorize** button on the right, using the token received from GitHub in 
the previous step, so it would be automatically added to query headers after.

### Queries

There are a LOT of people starring a LOT of repositories on GitHub... Resulting in our queries targeting heavy datasets.
The application is using both caching (Redis) and paging (with maximum page size), yet debug messages make it clear why
it takes a **long time** to get a query response even for less "heavyweight" repositories.

The current algorithm clearly should be improved.


### Development, testing

The Application is providing a handy dev environment using Tox.

All checks ('lint', 'type', 'test') can be launched as a single `tox` command.

Underlying tools are `pyright`, `mypy`, `uv` and `ruff`.


### TODO

- Potential query limits should be introduced
  - Idea: Perhaps: offline processing...?
- The application output is not using limits/paging yet.
  - Note: Unfortunately with the current algorithm the whole dataset has to be processed before returning results. Thus paging won't improve execution time.
- Authentication should be set up for Redis
- Investigating async/threading options
  - Note: [GitHub is discouraging "hammering" on the endpoints](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api?apiVersion=2022-11-28)
- Currently only public repositories are taken into account. However the authenticated user should be able to query more (though superficial check may not confirm this theory). To be investigated.



