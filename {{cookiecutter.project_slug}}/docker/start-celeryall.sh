#!/bin/sh
cd src
rm -rf celerybeat.pid celerybeat-schedule
nohup celery -A apps.taskapp worker -l INFO &
nohup celery -A apps.taskapp beat -l INFO &
celery -A apps.taskapp flower
