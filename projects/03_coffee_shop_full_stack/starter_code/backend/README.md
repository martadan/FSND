# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
https://dev-l4529u72.auth0.com/authorize?audience=coffee&response_type=token&client_id=dRZH6O0PRKaO2Lhwm05EmROtKSWm6Ozp&redirect_uri=http://localhost:8080/login-results
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
        - barista@test.com, BARISTAtest20
        - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhNDU4NzI1NGIxNGMwYzEyNTZhOTcwIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg4MjA5ODk4LCJleHAiOjE1ODgyMTcwOTgsImF6cCI6ImRSWkg2TzBQUkthTzJMaHdtMDVFbVJPdEtTV202T3pwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6ZHJpbmtzLWRldGFpbCJdfQ.VaGz-9JrpHGy4V_bPJWZve9sWM26y6v3zq2g70V1BgTzOUfCU41RkTClMNEsqqabogcEypec4LcTI-LtQlm7SptVZcsoAFBDGhI17RxW-jgexts10Gp4Kk6X-GqxTNH__NPEwDhtJEhSjXhHAfeSt8MWhCr2_DA83TRZRwqWWFDG8GzSk4-lyl6tX453PSdiucNszpkzVQ7elTK9POKZUBAtBYWp1ZRyTQlUaNZJZ0ph9AP0NdZh8lGZDwAlk9iKlue4-dZHsI5H-48pQCRLhTYj5feDCstscM9xYa0MiqSIWbARn5wdRhr4iKFFQnnd2FFI_p97RwXd-oNiAebPtw
    - Manager
        - can perform all actions
        - manager@test.com, MANAGERtest20
        - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhNDU5NGE1NGIxNGMwYzEyNTZhYjY2IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg4MjA5ODQ5LCJleHAiOjE1ODgyMTcwNDksImF6cCI6ImRSWkg2TzBQUkthTzJMaHdtMDVFbVJPdEtTV202T3pwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcy1kZXRhaWwiLCJwYXRjaDpkcmlua3MiLCJwb3N0OmRyaW5rcyJdfQ.iyOU-4IyHVPRIkv1nny5bVJ7OFGkX7BxPpcyttymyRDegJVzckItwjWV0Og3YGMhibzOcd5sHxbaraqx8VUjpct429wgXn3n3y2XTy1RuI76QQNlMjzmkoYYC-W2Kg-ygNSK41-my0fxberUu2k8KkC44ZnsWfD4iohIWeqBTnD7iPQlMzNXHRtT55dosvs62TUJ8S0R5GONpTexh-RPhn2buzYXEwM90h8b6_z7zgxVeom3Un-XLW71GqPhp8qW3PzkbbkeY7Wg-kn4hac-v4SIPnwTZbplpu0aEo8idc2ZLwsE1y20Nb3u6qu8ZBkLPi-z8xxHUFpb0YesjoMg3Q
7. Test your endpoints with [Postman](https://getpostman.com).
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
