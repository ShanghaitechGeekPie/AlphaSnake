# AlphaSnake
AlphaSnake

## Deployment

```bash
docker build -t geekpie/alphasnake .
docker run -e CLIENT_SOCKET_SERVER_URL=127.0.0.1:3000 \
           -e SOCKET_SERVER_URL=socketserver:3000 \
           -e SERVER_URL_BASE=http://127.0.0.1:8000 \
           -e SECRET_KEY=$secret_key \
           -e ROUND_TIME_SLICE=10 \
           -p 8000:8000 geekpie/alphasnake
```

### Socket Server URL

`CLIENT_SOCKET_SERVER_URL`: external URL working for client browsers
`SOCKET_SERVER_URL`: docker-compose internal URL working for QJ and backend

### SECRET_KEY

Create random key using this python snippet, no need to change for every restart. NEVER leak this key!

```python
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
```
### TODO

- build frontend assets
- db env
- wsgi
- upgrade to django 2.0

