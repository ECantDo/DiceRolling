import random


def roll_large_dice(num_dice, sides):
    mean = num_dice * (sides + 1) / 2
    variance = num_dice * ((sides ** 2 - 1) / 12)
    stddev = variance ** 0.5
    return int(random.gauss(mean, stddev))


def compute_roll(dice_number: int, dice_sides: int = 6):
    print(f"Expected: {dice_number * ((1 + dice_sides) / 2)}")
    print(f"Result: {roll_large_dice(dice_number, dice_sides)}")
    pass
