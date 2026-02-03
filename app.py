import time
import redis # type: ignore

from flask import Flask # type: ignore

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)
            
@app.route('/')
def hello():
    count = get_hit_count()
    return 'Hello! This page has been visited {} times.\n'.format(count)