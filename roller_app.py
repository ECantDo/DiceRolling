import dice_logic

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

        dice_logic.compute_roll(number, sides)
        print()
