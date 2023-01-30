#!/bin/sh
cd Assesment/app/
celery --app app.tasks.celery beat
