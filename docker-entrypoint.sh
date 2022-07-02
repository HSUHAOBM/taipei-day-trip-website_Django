#!/bin/sh
echo 'Run migration'

python3 manage.py makemigrations order
python3 manage.py makemigrations member
python3 manage.py makemigrations trip_data
python3 manage.py migrate
cd  trip_data
python json_data_load.py
pwd
