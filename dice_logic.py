# file dice_logic.py

import random
import hmac
import hashlib
import json
import time
from pathlib import Path
from typing import Optional


def roll_large_dice(num_dice, sides) -> int:
    mean = num_dice * (sides + 1) / 2
    variance = num_dice * ((sides ** 2 - 1) / 12)
    stddev = variance ** 0.5
    return int(random.gauss(mean, stddev))


def roll_small_dice(num_dice, sides) -> int:
    sum = 0
    for _ in range(num_dice):
        sum += random.randint(1, sides)

    return sum


def roll_dice(num_dice, sides) -> int:
    if num_dice < 1:
        return -1

    split = 10
    if num_dice > split:
        return roll_large_dice(num_dice, sides)

    return roll_small_dice(num_dice, sides)


def sign_entry(entry: dict, secret_key: bytes) -> str:
    entry_to_sign = {k: v for k, v in entry.items() if k != "signature"}
    msg = json.dumps(entry_to_sign, sort_keys=True, separators=(",", ":")).encode()
    signature = hmac.new(secret_key, msg, hashlib.sha256).hexdigest()
    return signature


def append_log(entry: dict, log_file: Path):
    line = json.dumps(entry, separators=(",", ":")) + "\n"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(line)
        f.flush()
        try:
            import os
            os.fsync(f.fileno())
        except Exception:
            pass


def verify_entry_signature(entry: dict, secret_key: bytes) -> bool:
    signature = entry.get("signature")
    if not signature:
        return False
    expected = sign_entry(entry, secret_key)
    return hmac.compare_digest(signature, expected)
