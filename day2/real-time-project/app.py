import os
from datetime import datetime, timezone

from flask import Flask, jsonify


APP_VERSION = os.getenv("APP_VERSION", "1.0")
APP_ENV = os.getenv("APP_ENV", "production")

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify(
        {
            "service": "barisagar-health-api",
            "message": "Docker Day 2 Python API is running",
            "endpoints": ["/health", "/ready", "/version"],
        }
    )


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "ok",
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/ready")
def ready():
    return jsonify(
        {
            "ready": True,
            "dependency_check": "passed",
        }
    )


@app.get("/version")
def version():
    return jsonify(
        {
            "version": APP_VERSION,
            "environment": APP_ENV,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
