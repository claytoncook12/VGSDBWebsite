# www.VGSDB.com

This is a website that keeps track of tunes that have been played on Shannon and Matt Heatons Online Irish Session.

The project uses Django and MySQL Database deployed to a cPanel site management platform.

Take a look at the site here, www.vgsdb.com.

# Steps for running locally
## Docker commands to Build and Run the Database Locally

Build the needed MySQL database. Will be in `DjangoApp/data/db` when run. 
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
python DjangoApp/manage.py runserver
```