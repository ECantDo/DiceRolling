# file: server_module.py
import base64
from datetime import datetime, timezone
import queue

from flask import Flask, request, jsonify
import os
import json
import secrets
import string
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


# ======================================================================================================================
# DM server stuff
# ======================================================================================================================
_connected_clients = {}  # {client_token: {<Client Data>}}


def _generate_code(length: int):
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(length))


def _generate_client_token():
    return secrets.token_urlsafe(32)


_SESSION_PASSWORD = _generate_code(8)  # The password to give to the DM's to get a logs access token
print(f"{_SESSION_PASSWORD = }")  # TODO: Make it more secure displaying of the token


@app.route("/dm-login", methods=["POST"])
def dm_login():
    data = request.get_json()
    session_call = data.get("password", None)

    if session_call is not None:
        password = session_call.get("password")
        if password is None or password != _SESSION_PASSWORD:
            return jsonify({"error": "Invalid password"}), 401
        # Do valid password logic here
        client_token = _generate_client_token()
        last_sig: str = _get_last_log_signature(LOG_FILE)
        _connected_clients[client_token] = {
            "username": session_call.get("username"),
            "last_signature": last_sig
        }
        return jsonify({
            "client_token": client_token,
            "last_signature": last_sig
        }), 200
        pass

    session_call = data.get("session", None)
    if session_call is not None:
        token: str = session_call.get("token")
        if token is None or token not in _connected_clients:
            return jsonify({"error": "Invalid token"}), 403
        # Do valid token logic here
        signature: str = session_call.get("signature")
        # TODO: Use the below functions to finish
        payload: dict = {

        }
        current_last = _get_last_log_signature(LOG_FILE)
        if signature is None:
            payload["last_signature"] = current_last
            payload["logs"] = []
        else:
            if current_last != signature:
                payload["logs"] = _fetch_new_logs(LOG_FILE, signature)
                payload["last_signature"] = payload["logs"][-1]["signature"]
            else:
                payload["logs"] = []
                payload["last_signature"] = current_last
            pass

        return jsonify(payload), 200

    return jsonify({"error": "Unknown"}), 400
    pass


def _get_last_log_signature(file_path: Path) -> str | None:
    with file_path.open("rb") as f:
        f.seek(0, 2)  # go to end of file
        if f.tell() == 0:
            return None  # empty file

        buffer = b""
        pointer = f.tell() - 1

        # walk backwards until we hit a newline or BOF
        while pointer >= 0:
            f.seek(pointer)
            byte = f.read(1)
            if byte == b"\n" and buffer:
                break
            buffer += byte
            pointer -= 1

        # reverse since we built it backwards
        last_line = buffer[::-1].decode("utf-8")
        last_entry = json.loads(last_line)
        return last_entry.get("signature")


def _fetch_new_logs(file_path: Path, last_signature: str):
    new_logs = []
    with file_path.open("rb") as f:
        f.seek(0, 2)
        if f.tell() == 0:
            return []  # empty file

        buffer = b""
        pointer = f.tell() - 1

        while pointer >= 0:
            f.seek(pointer)
            byte = f.read(1)

            if byte == b"\n":
                if buffer:
                    line = buffer[::-1].decode("utf-8")
                    buffer = b""
                    log_entry = json.loads(line)

                    if log_entry.get("signature") == last_signature:
                        break  # stop once we hit the last known signature
                    new_logs.insert(0, log_entry)
            else:
                buffer += byte

            pointer -= 1

        # handle very first line if no trailing newline
        if buffer:
            line = buffer[::-1].decode("utf-8")
            log_entry = json.loads(line)
            if log_entry.get("signature") != last_signature:
                new_logs.append(log_entry)

    return new_logs


# ======================================================================================================================
# Rolling server stuff
# ======================================================================================================================
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
               f"Timestamp: {get_local_time(timestamp)}"])
    return jsonify(entry)


def get_local_time(utc_timestamp: str) -> str:
    utc_dt = datetime.fromisoformat(utc_timestamp)
    local_dt = utc_dt.astimezone()  # Converts to local timezone
    return local_dt.strftime("%Y-%m-%d ~ %I:%M:%S %p")


def run_server(log_q):
    global SECRET_KEY, log_queue  # The secret key is for hashing
    log_queue = log_q

    key_b64 = os.environ.get("DICE_LOG_SECRET")
    if not key_b64:
        raise RuntimeError("DICE_LOG_SECRET environment variable not set")

    SECRET_KEY = base64.urlsafe_b64decode(key_b64)

    app.run(host="0.0.0.0", port=5000)
