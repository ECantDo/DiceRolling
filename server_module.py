# file: server_module.py
import base64

from flask import Flask, request, jsonify
import os
import time
from pathlib import Path
from dice_logic import roll_dice, sign_entry, append_log

app = Flask(__name__)
LOG_FILE = Path("roll_log_server.ndjson")

SECRET_KEY = b"this is not a valid key"


@app.route("/roll", methods=["POST"])
def roll_endpoint():
    print("Received roll request:", request.json)

    data = request.json
    player = data.get("player", "Unknown")
    try:
        num_dice = int(data.get("num_dice"))
        num_sides = int(data.get("num_sides"))
        if num_dice < 1 or num_sides < 2:
            raise ValueError
    except Exception:
        return jsonify({"error": "Invalid dice parameters"}), 400

    dice, result = roll_dice(num_dice, num_sides)
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    entry = {
        "timestamp": timestamp,
        "player": player,
        "num_dice": num_dice,
        "num_sides": num_sides,
        "result": result,
        "dice": dice,
        "faces": num_sides
    }

    signature = sign_entry(entry, SECRET_KEY)
    entry["signature"] = signature

    append_log(entry, LOG_FILE)
    return jsonify(entry)


def run_server():
    # context = ('cert.pem', 'key.pem')  # Use your SSL cert and key here
    # app.run(host="0.0.0.0", port=5000, ssl_context=context)
    global SECRET_KEY

    key_b64 = os.environ.get("DICE_LOG_SECRET")
    if not key_b64:
        raise RuntimeError("DICE_LOG_SECRET environment variable not set")

    SECRET_KEY = base64.urlsafe_b64decode(key_b64)

    app.run(host="0.0.0.0", port=5000)
