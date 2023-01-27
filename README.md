# Quickstart

1. Make sure port `8888` is open
2. Run `docker compose up` to start the app
3. Apply migrations `docker compose run web python manage.py migrate`
4. Run `docker compose restart faust` (found a bug in Faust on PY3.11, already reported to the devs)
5. Send some data

```
curl -v --location --request POST 'http://localhost:8888/items/' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
    "external_id": "0xdeadbeef",
    "name": "lcamtuf",
    "value": 1337
}'
```

# Overview

> You may assume that there is some kind of javascript code placed in various stores that
> will feed the data to our tracker (according to the specification listed below).


> Returns - 204 No Content

Tracking tools are transparent to end users so, I can defer the process of saving a record effectively making the `/items/` endpoint sql-less (if the user has an active cart assigned to the session)


# Performance

tl;dr

`docker compose -f docker-compose.locust.yaml up --scale worker=4`
then go to `http://localhost:8089` or see the report at [docs/locust_report.html](docs/locust_report.html)


# Code style

see `.pre-commit-config.yaml` 


# Tests

Run `docker compose run web pytest` to tests the app

