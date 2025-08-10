# roller_app.py
import tkinter as tk
from tkinter import messagebox
from dice_logic import compute_roll, roll_large_dice  # replace with your actual filename


def on_roll():
    try:
        num_dice = int(entry_dice.get())
        num_sides = int(entry_sides.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter whole numbers for both fields.")
        return

    # Calculate expected value and result
    expected = num_dice * ((1 + num_sides) / 2)
    result = roll_large_dice(num_dice, num_sides)

    label_result.config(text=f"Expected: {expected:.2f}\nResult: {result}")


root = tk.Tk()
root.title("Large Dice Roller")

# Number of dice
tk.Label(root, text="Number of Dice:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
entry_dice = tk.Entry(root)
entry_dice.grid(row=0, column=1, padx=5, pady=5)

# Sides per die
tk.Label(root, text="Sides on Dice:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
entry_sides = tk.Entry(root)
entry_sides.grid(row=1, column=1, padx=5, pady=5)

# Roll button
tk.Button(root, text="Roll", command=on_roll).grid(row=2, column=0, columnspan=2, pady=10)

# Result label
label_result = tk.Label(root, text="", font=("Arial", 12))
label_result.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()
