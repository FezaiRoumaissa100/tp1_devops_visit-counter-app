import os
import socket
from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host=os.getenv("REDIS_HOST", "db-service"), port=6379, decode_responses=True)

@app.route("/")
def index():
    hits = r.incr("hits")
    container_id = socket.gethostname()
    return f"Bonjour ! Cette page a été vue {hits} fois. Je suis le conteneur {container_id}\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
