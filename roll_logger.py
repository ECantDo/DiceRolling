import hmac, hashlib, json, time

SECRET_KEY = b"YOUR_SECRET_KEY_HERE"  # Keep private


def log_roll(player_name, num_dice, num_sides, result, logfile="roll_log.json"):
    timestamp = time.time()
    data = {
        "timestamp": timestamp,
        "player": player_name,
        "num_dice": num_dice,
        "num_sides": num_sides,
        "result": result
    }
    # Create a signature
    msg = json.dumps(data, sort_keys=True).encode()
    signature = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
    data["signature"] = signature

    try:
        with open(logfile, "r") as f:
            logs = json.load(f)
    except FileNotFoundError:
        logs = []
    logs.append(data)
    with open(logfile, "w") as f:
        json.dump(logs, f, indent=2)


def verify_log_entry(entry):
    signature = entry.pop("signature", None)
    msg = json.dumps(entry, sort_keys=True).encode()
    expected = hmac.new(SECRET_KEY, msg, hashlib.sha256).hexdigest()
    return signature == expected
