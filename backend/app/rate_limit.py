from fastapi import HTTPException, Request

from app.cache import redis_client

REQUEST_LIMIT = 3
WINDOW = 300


def rate_limit(request: Request):

    client_ip = request.client.host

    key = f"rate_limit:{client_ip}"

    current = redis_client.get(key)

    if current:
        current = int(current)

        if current >= REQUEST_LIMIT:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        redis_client.incr(key)

    else:
        redis_client.setex(key, WINDOW, 1)
