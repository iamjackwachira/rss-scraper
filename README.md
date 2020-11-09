# RSS Scraper
Simple RSS scraper application which saves RSS feeds to a database and lets a user view and manage feeds they’ve added to the system through an API.


## Run locally via Docker

Build first the images and run the webserver on port 8080:

```shell
$ docker-compose up --build # --no-cache to force deps installation
```

To run the tests:

```shell
$ docker-compose run --entrypoint '/usr/bin/env' --rm rss_web pytest # --keepdb to run faster
```

To run bash:

```shell
$ docker-compose run --entrypoint '/usr/bin/env' --rm rss_web bash
```

or if you initialized already a container:

```shell
$ docker exec -it rss_web bash
```

To connect to the database when the container is running:

```shell
$ docker exec -it rss_postgres psql -U root postgres
```

## Development
To install flake8 hooks for PEP8 checking:
```shell
$ pre-commit install
```

Optionally run
```shell
$ pre-commit run --all-files
```

Create a new `.env` file from `.env.sample` with appropriate values for the secrets

## API Docs
After running the app, go to `localhost:8000/docs/` to access swagger docs