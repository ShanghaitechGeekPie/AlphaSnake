#!/bin/sh

python manage.py migrate

python manage.py runserver 0.0.0.0:8000 &

# wait for startup. todo: use wsgi
sleep 5

cd AlphaSnakeCentrol
while true; do
    echo Starting QJ
    python QJ.py
    echo QJ quited, sleep 30s
    sleep 30
done
