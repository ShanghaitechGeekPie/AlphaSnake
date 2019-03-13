FROM python:3.7

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY AlphaSnakeCentrol/ .
COPY launch.sh ./

ENV SOCKET_SERVER_URL=127.0.0.1:3000
ENV SERVER_URL_BASE=http://127.0.0.1:8000

ENV ROUND_TIME_SLICE=10

# TODO: build frontend assets

EXPOSE 8000

CMD sh launch.sh

