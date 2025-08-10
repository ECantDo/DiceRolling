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


def compute_roll(dice_number: int, dice_sides: int = 6):
    print(f"Expected: {dice_number * ((1 + dice_sides) / 2)}")
    print(f"Result: {roll_large_dice(dice_number, dice_sides)}")
    pass
