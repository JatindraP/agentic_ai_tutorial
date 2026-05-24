from redis import Redis
from rq import Queue

import rag_utils as utils

REDIS_HOST = utils.get_config("valkey", "host")
REDIS_PORT = utils.get_config("valkey", "port")

def get_rq_queue():
    """
    This function initializes a connection to the Redis server and creates an RQ queue named 'default'.
    It returns the queue object that can be used to enqueue tasks for asynchronous processing.
    """
    redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT)
    rq_queue = Queue('default', connection=redis_conn)
    print(f"Connected to Redis at {REDIS_HOST}:{REDIS_PORT} and initialized RQ queue 'default'.")
    return rq_queue