from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/health")
def health():
    return jsonify(status="healthy"), 200

@app.route("/api")
def api():
    return jsonify(message="Hello from NexusDeploy", version=os.getenv("APP_VERSION", "v1")), 200

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=3000)