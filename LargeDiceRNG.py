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


if __name__ == "__main__":
    while True:
        number = input("Number of dice: ")
        try:
            number = int(number)
        except Exception as e:
            if number.lower == "exit":
                break
            print("Number was not a number...")
            continue
            pass
        sides = input("Sides on Dice: ")
        try:
            sides = int(sides)
        except Exception as e:
            if sides.lower() == "exit":
                break
            print("Sides was not a number...")
            continue

            pass

        compute_roll(number, sides)
        print()
    pass
