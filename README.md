# VGSDB.com

This is a website that keeps track of tunes that have been played on Shannon and Matt Heatons Online Irish Session.

The project uses Django and Postgres.

## Docker commands to build and run docker containers locally in development environment

Build the needed files for the Postgres database and shut back down. Will be  in `DjangoApp/data` when run. 
```
docker compose -f docker-compose.dev.yml up -d db
docker compose -f docker-compose.dev.yml down db
```

Now the database files are created can run all containers.
```
docker compose -f docker-compose.dev.yml up -d
```

## Commands to Create and Load Django Fixtures

To export data in Session app data
```
python manage.py dumpdata session > 2021-08-18sessionapp.json
```

To export import Session app data
```
python manage.py loaddata session 2021-08-18sessionapp.json
```