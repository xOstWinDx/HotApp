#!/bin/bash

if [[ "${1}" == "celery" ]]; then
  celery --app=app.tasks.celeryConf:celery worker -l INFO
elif [[ "${1}" == "flower" ]]; then
               app/tasks/celeryConf.py
  celery --app=app.tasks.celeryConf:celery flower
fi