
# Django-FastAPI-Angular-Celery ChatApp

This project is developed on multiple technologies
Django used for main backend and Django channels for Websocket
FastAPI for Auth REST-API's with django ORM and django utilities
Celery with Redis for background task scheduling and cron jobs
Angular for frontend web ChatApp



## Installation

Use python v3.9
NodeJs v21.0
Angular v16
Redis server should be running on redis://127.0.0.1:6379/0

Setup and activating python environment in the project directory

```bash
  python -m venv env
  env/scripts/activate
```
come back to project directory and install dependencies

```bash
  pip install -r req.txt
```
Note! run the below commands and seperate terminals and make sure the environment should be activate.

run the fastapi app 
```bash
  python main.py
```

run the django app 
```bash
  python manage.py runserver
```

run the celery server
```bash
  celery -A core worker -l info  
```


install the node modules and run the angular frontend
```bash
  cd frontend
  npm install  
  ng serve
```