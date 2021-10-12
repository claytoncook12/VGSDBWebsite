# www.VGSDB.com

This is a website that keeps track of tunes that have been played on Shannon and Matt Heatons Online Irish Session.

The project uses Django and Postgres deployed to docker container running on AWS Elastic Beanstalk.

Take a look at the site here, www.vgsdb.com.

# Steps for running locally
## Docker commands to Build and Run the Database Locally

Build the needed Postgres database. Will be  in `DjangoApp/data` when run. 
```
docker compose -f docker-compose.dev.yml up -d db
```

Now the database is up an running. Next will be to setup a virtual enviornment and run the python development server
```
python -m venv venv
# If Windows
venv\scripts\activate
# If Ubuntu
source venv/bin/activate
# Install requirements
pip install -r DjangoApp\requirements.txt

# Run Django Developemnt Server
python DjangoApp/manage.py runserver 0.0.0.0:8000
```

## Running Database and Server Locally in Containers

If you wish to run both the database and server in a production setup, first settings have to updated in `DjangoApp/core/settings.py`. `HOST` should be updated to `db` and `PORT` should be updated to `5432` as below.

```
# DjangoApp/core/settings.py
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'postgres',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'db', #db or localhost
            'PORT': 5432, #5432 or 6543
        }
    }
```

Now you can run the command below to build and start the database and server within docker compose.

```
docker compose -f docker-compose.dev.yml up -d
```

Now you can access the runninng containers at localhost:8000.