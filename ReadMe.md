# Commuter Rail Departure

## Description
This is a simple Django application to display a commuter rail departure board.

## Important information
-- if a prediction has been found to match the schedule, the has_prediction will be true and the frontend will display the text as blue

## Resources
https://www.mbta.com/developers

## Improvements
In order to scale this application to more users it would be essential to not hit the MBTA api for every request to see a Stop's schedule and predictions. In order to achieve this it would be useful to automate the retrieveal of this data and store it in the applications database. This would allow the application to pull the data from its own database to server to users. In order to achieve such scale I would propose the usage of celery to automate the retrieval and storage of this data. This can be done by scheduling tasks to run every n number of minutes.

## Technology Stack
- **Python**: 3.10
- **Django**: 4.2.9
- **Database**: PostgreSQL

## Installation
Navigate to project directory.
```
sudo apt-get install libcurl4-openssl-dev
python -m venv venv
source ./venv/bin/activate
pip install wheel
pip install -e .
```

### Setup
```cp exampleenv.txt .env```

### Create Database
```
psql -U postgres
CREATE DATABASE commuter_rail_departure;
CREATE USER commuter_rail_departure WITH ENCRYPTED PASSWORD 'Testing321';
GRANT ALL PRIVILEGES ON DATABASE commuter_rail_departure TO commuter_rail_departure;
```

# Migrate database
```python manage.py migrate```

# Run Django server
```python manage.py runserver```
