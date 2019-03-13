#!/bin/sh

python manage.py migrate

mkdir -p static
cp frontend/viewer/public/socket.io.js static/socket.io.js
cat frontend/viewer/public/bundle.js | python -c "print(input().replace('http://127.0.0.1:3000', '${SOCKET_SERVER_URL}'))" > static/bundle.js

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
