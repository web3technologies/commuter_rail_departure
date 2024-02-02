# Commuter Rail Departure

## Description
This is a simple Django application to display a commuter rail departure board.

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
