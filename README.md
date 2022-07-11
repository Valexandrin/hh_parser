# HeadHunter parser

The service is designed for automatically vacancies collecting according to preferencies from resourse `https://hh.ru`

![Alt-текст](https://github.com/Valexandrin/hh_parser-frontend/blob/main/index.png?raw=true)|
:-:

## Project structure

The service consists on three parts: worker, backend and frontend. All these parts and database as well are running in docker container.
Worker regularly requests `https://api.hh.ru` for vacancies which match to preferencies and interact with backend for keep database up-to-date. Frontend shows vacancies with actual status (new/seen/like) and allows to see detailed descrition for chosen vacancy.
For running on localhost in docker container need to clone these resources into one directory:

```bash
git clone https://github.com/Valexandrin/hh_parser-worker.git
git clone https://github.com/Valexandrin/hh_parser-backend.git
git clone https://github.com/Valexandrin/hh_parser-frontend.git
```

## Start up

### One-time action (if not poetry)

```bash
pip install poetry
poetry config virtualenvs.in-project true
source .env\Scripts\activate
```

### Install dependecies

```bash
poetry init
poetry install
```

### Configure environment

Use `.env.default` to create `.env`

### Create database (backend)

```bash
make db.run
make db.create
```

## Usage

### for running docker container (backend)

```bash
make parse.run
```

..and go to `http://127.0.0.1:5000/`

### for running a resource independently

```bash
make run
```

## Resources used

```bash
PostgreSQL - database management system (DBMS)
httpx - fully featured HTTP client for Python 3
pydantic - data validation and settings management
sqlalchemy - lib. Work with different DBMS
psycopg2-binary - lib. Work with PostgreSQL (multi-threaded applications)
alembic - database migrations tool
orjson - fast, correct JSON library for Python
```
