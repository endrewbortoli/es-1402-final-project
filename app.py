
import os
import secrets
from flask import Flask, render_template, request, jsonify
from servo_controller import ServoController

app = Flask(__name__)
controller = ServoController()

CONTROL_TOKEN = os.environ.get("LOCK_TOKEN")

if not CONTROL_TOKEN:
    raise RuntimeError("Set LOCK_TOKEN before starting the server")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/status")
def status():
    return jsonify({
        "state": controller.state,
        "simulation": controller.servo is None
    })

@app.route("/api/control", methods=["POST"])
def control():
    token = request.headers.get("X-Lock-Token", "")

    if not secrets.compare_digest(token, CONTROL_TOKEN):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True) or {}
    action = data.get("action")

    if action not in ("locked", "unlocked"):
        return jsonify({"error": "Invalid action"}), 400

    state = controller.move(action)
    return jsonify({"state": state})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
