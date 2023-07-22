# Hacks-Web-Backend
Hack Web Python - Django project

## Setup

`python -m pip install -r requirements.txt`

### ./my.cnf
```
[client]
host = HOST
database = NAME
user = USER
password = PASSWORD
default-character-set = utf8
```

### startup scripts
`python manage.py migrate`

## Running Hacks
`python manage.py runserver`

## Development
### Model changing
When done run `python manage.py makemigrations <app_name>` to create migration scripts

After which run `python manage.py migrate` to execute migrations
