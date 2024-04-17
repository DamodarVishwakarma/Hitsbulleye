# HBE-TEST-API
## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Built Using](#built_using)
- [Contributing](../CONTRIBUTING.md)

## 🧐 About <a name = "about"></a>

This application will serve APIs to Hitbullseye web application.

## 🏁 Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.

### Prerequisites

1. [Python](https://www.python.org/downloads/release/python-390/)
2. [Pipenv](https://pypi.org/project/pipenv/)
3. [Redis](https://redis.io/)


--------------
## Setup Process

- create and setup the virtual env for [python](https://docs.python.org/3/library/venv.html).
- install all the dependencies in venv : this command will use the already present Pipfile to install dependencies.
    ```bash
    pipenv install
    ```
- create a database and then either store the credentials in global variable from terminal, or create a .env file and store them there. This is required by alembic to make db connection.
- Optional : if alembic version is not present, generate one.
    ```bash
    alembic -c ./src/alembic.ini revision --autogenerate -m "1st version"
    ```
- create database schema using alembic
    ```bash
    alembic -c ./src/alembic.ini upgrade head
    ```
    if there are any error in this command check
    - database connection and credentials
    - already present schema
- run the fastapi server
    ```bash
    uvicorn --reload src.main:app
    ```
    ** mac users remove --reload form above command if it keeps reloading
    

### Installing

Clone the repository

```
https://github.com/hbe-tech/HBE-TEST-APP-API.git
```

Create virtual environment and add project dependencies to it

```
pipenv install
```

Activate virtual environment

```
pipenv shell
```

Run database migration scripts

```
alembic -c ./src/alembic.ini upgrade head
```

Run application

```
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## ⛏️ Built Using <a name = "built_using"></a>

- [Postgres](https://www.postgresql.org/) - Database
- [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- [Uvicorn](https://www.uvicorn.org/) - Application Server
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Migration tool
- [Aioredis](https://aioredis.readthedocs.io/en/latest/) - Redis Library
