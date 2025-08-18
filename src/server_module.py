# file: server_module.py
import base64
from datetime import datetime, timezone
import queue

from flask import Flask, request, jsonify
import os
import time
from pathlib import Path
from dice_logic import roll_dice, sign_entry, append_log, expected_roll

app = Flask(__name__)
LOG_FILE = Path("./roll_log_server.ndjson")

log_queue: queue.Queue | None = None

SECRET_KEY = b"this is not a valid key"


def log_event(msg):
    if log_queue is None:
        print("Queue not initialized...")
        return

    # print(msg)
    if log_queue:
        log_queue.put(msg)


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
    except ValueError:
        return jsonify({"error": "Invalid dice parameters"}), 400

    dice, result = roll_dice(num_dice, num_sides)
    timestamp = datetime.now(timezone.utc).isoformat()

    entry = {
        "timestamp": timestamp,
        "player": player,
        "num_dice": num_dice,
        "num_sides": num_sides,
        "result": result,
        "dice": dice,
        "version": data["version"]
    }

    signature = sign_entry(entry, SECRET_KEY)
    entry["signature"] = signature

    append_log(entry, LOG_FILE)
    log_event([(player, result, num_dice, num_sides),
               f"{dice}\nExpected Value: {expected_roll(num_dice, num_sides)}\n"
               f"Timestamp: {_display_local_time(timestamp)}"])
    return jsonify(entry)


def _display_local_time(utc_timestamp: str) -> str:
    utc_dt = datetime.fromisoformat(utc_timestamp)
    local_dt = utc_dt.astimezone()  # Converts to local timezone
    return local_dt.strftime("%Y-%m-%d ~ %I:%M:%S %p")


def run_server(log_q):
    # context = ('cert.pem', 'key.pem')  # Use your SSL cert and key here
    # app.run(host="0.0.0.0", port=5000, ssl_context=context)
    global SECRET_KEY, log_queue
    log_queue = log_q

    key_b64 = os.environ.get("DICE_LOG_SECRET")
    if not key_b64:
        raise RuntimeError("DICE_LOG_SECRET environment variable not set")

    SECRET_KEY = base64.urlsafe_b64decode(key_b64)

    app.run(host="0.0.0.0", port=5000)
