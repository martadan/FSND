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
        - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhNDU4NzI1NGIxNGMwYzEyNTZhOTcwIiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg3ODI4ODc3LCJleHAiOjE1ODc4MzYwNzcsImF6cCI6ImRSWkg2TzBQUkthTzJMaHdtMDVFbVJPdEtTV202T3pwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.g6uN4x614WheOO4enIhuzTg6zX7-ucWCaioKf0XtG1Te79VzSEDCNWXh_rs17FAm4uUMtG1enRQclYF2Dit_dRjnCsj1jwMGR2vL1uV3mKP_mpvwd7kuuo2g4bS8fdnDx6ejZB7Pq760kqcB20YQU3KuDvmBTw5zaG4cEvjlgyQc7M8FBALG5fTb4Xc5bByWB5UFXB82BvusrfblNVs5e0BCKYRTSMMKtPc4ujxuMCB8mhdqPLRRAvHX7czF_bgEc2dDgzk30AHSLvie-fRLg0GhZIb55-AZ39QFcsl-d3kUC_gecCCVVe_F5Vh0x5o1LLNwYHX13Z7NmAX70q64ug
    - Manager
        - can perform all actions
        - manager@test.com, MANAGERtest20
        - eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFKOW9HX3R5eHlHcG1Ub1ZVNlRSTiJ9.eyJpc3MiOiJodHRwczovL2Rldi1sNDUyOXU3Mi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVhNDU5NGE1NGIxNGMwYzEyNTZhYjY2IiwiYXVkIjoiY29mZmVlIiwiaWF0IjoxNTg3ODI5MDgzLCJleHAiOjE1ODc4MzYyODMsImF6cCI6ImRSWkg2TzBQUkthTzJMaHdtMDVFbVJPdEtTV202T3pwIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.keiv2OQkcF0ZzOWrn7czv4wtG92HkK9Q0mbmRLEeoDPaZZsC3Id_qB36ROJFfeF6a9mKdHuRyJPn4GnnI5I_PJ6kQ11JzT7aViXzwCc3tbFjY6GnUNcdqykQaKCNPdB_2LJ4b8agKLDhOpwf3NRzijR4O9Jjr32m07MX1fAHLhRgNsLWu58Y8ePxoJ7bfLduY6u8B0qEp1c3iBV3WLzofd0TN42DeD7YzaLcoemOwiCdCw2XaMgcH_3Ja_Ej_8IZhNmna3bHKuYorEDkzfqQ3zpetyn8VM1qkUuHbqhWtnkiNeqOirmLg4XZCVa5HbXBA_tDjJIKduxdhv1A3zv2BA
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
