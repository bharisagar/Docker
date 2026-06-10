from flask import Flask
import redis

app = Flask(__name__)

redis_client = redis.Redis(
    host='redis',
    port=6379,
    decode_responses=True
)

@app.route("/")
def home():

    count = redis_client.incr("visits")

    return f"Welcome to Docker Compose! Visits: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)