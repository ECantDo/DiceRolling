import random
import customtkinter as ctk
from PIL import Image
from PIL import ImageTk
import os

import roller_app


class SingleDiceRollerFrame(ctk.CTkFrame):
    def __init__(self, master, dice_faces: list[str] | list[ImageTk.PhotoImage], roll_duration: int = 800,
                 roll_interval: int = 80, **kwargs):
        """
        :param dice_faces: list of filepaths to dice face images, index 0 = face 1, etc., or a list of images
        :param roll_duration: total rolling animation time in ms
        :param roll_interval: how often to update face during roll in ms
        """
        super().__init__(master, **kwargs)

        # Load the images once
        if dice_faces is list[str]:
            self.dice_faces = [ImageTk.PhotoImage(Image.open(path).resize((128, 128))) for path in dice_faces]
        else:
            self.dice_faces = dice_faces

        transparent_path = roller_app.resource_path("assets/diceTransparent.png")
        self._transparent_dice = ImageTk.PhotoImage(Image.open(transparent_path))

        self.label = ctk.CTkLabel(self, image=self.dice_faces[0], text="")
        self.label.pack(padx=10, pady=10)

        self.rolling = False
        self.roll_duration: int = roll_duration
        self.roll_interval: int = roll_interval
        self.elapsed: int = 0
        self.previous_roll_face = None
        self.current_after_id = None

        pass

    def roll(self, result: int | None):
        if self.rolling:
            return  # already rolling

        self.rolling = True
        self.elapsed = 0
        self.current_after_id = None
        self.previous_roll_face = None

        if result is None:
            result = random.randint(1, 6)
        elif not (1 <= result <= 6):
            return  # Cant roll a die with more than 6, or less than 1 sides

        self._roll_animation(result)
        pass

    def _roll_animation(self, result: int):
        if self.elapsed >= self.roll_duration:
            # Roll finished
            self.label.configure(image=self.dice_faces[result - 1])
            self.rolling = False
            return

        # Random face "rolling"
        if self.previous_roll_face is None:
            face_idx = random.randint(0, 5)
        else:
            face_idx = random.randint(0, 4)
            if face_idx >= self.previous_roll_face:
                face_idx += 1

        self.previous_roll_face = face_idx

        self.label.configure(image=self.dice_faces[face_idx])

        self.elapsed += self.roll_interval
        self.current_after_id = self.after(self.roll_interval, lambda: self._roll_animation(result))
        pass

    def hide(self):
        self.label.configure(image=self._transparent_dice)
        pass

    def show(self):
        self.label.configure(image=self.dice_faces[self.previous_roll_face])
        pass


# For later use when adding more dice
__dice_face_indexing: tuple[int, int, int, int, int, int] = (4, 6, 8, 10, 12, 20)


class DiceApp(ctk.CTkFrame):
    def __init__(self, master, max_dice: int = 10, **kwargs):
        super().__init__(master, **kwargs)
        self.max_dice = max_dice
        self.container_width = 700
        self.container_height = 300
        self.dice_count = 1
        self.rolling = False

        # Load all images
        dice_folder = roller_app.resource_path('assets/d6')
        dice_paths = [os.path.join(dice_folder, f'dice{i}.png') for i in range(1, 7)]
        self.dice_frames = [ImageTk.PhotoImage(Image.open(path).resize((128, 128))) for path in dice_paths]

        # Make the frame
        self.dice_container = ctk.CTkFrame(self, width=self.container_width, height=self.container_height)
        self.dice_container.pack(pady=10)
        self.dice_container.pack_propagate(False)  # Fix size, don’t shrink to contents

        # Configure grid columns (5 columns)
        for i in range(5):
            self.dice_container.grid_columnconfigure(i, weight=1)

        # 2 rows max
        for r in range(2):
            self.dice_container.grid_rowconfigure(r, weight=1)

        self.dice_widgets: list[SingleDiceRollerFrame] = []
        for idx in range(self.max_dice):
            die = SingleDiceRollerFrame(self.dice_container, self.dice_frames)
            self.dice_widgets.append(die)

            row, col = _compute_dice_location(idx, self.max_dice)
            die.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        self.set_dice_count(0)
        pass

    def set_dice_count(self, count: int):
        if self.rolling:
            return
        count = max(0, min(count, self.max_dice))
        self.dice_count = count
        for i, die in enumerate(self.dice_widgets):
            if i < count:
                pass
            else:
                die.hide()  # hide dice

    def roll_dice(self, results: list[int] | None):
        """
        Roll all the dice with either a random outcome, or a pre-set outcome
        :param results: If None; will make all dice that exist roll randomly, otherwise, the dice will be remade, then
        rolled with the expected outcomes
        :return:
        """
        if self.rolling:
            return
        self.rolling = True
        if results is None:
            results = [None] * self.dice_count
        else:
            self.set_dice_count(len(results))

        for i, die in enumerate(self.dice_widgets):
            if i >= len(results):
                break
            die.roll(results[i])
        self.rolling = False
        pass

    pass


def _compute_dice_location(idx: int, count: int) -> tuple[int, int]:
    row = 0 if count <= 5 else (0 if idx < 5 else 1)
    if count == 1:
        col = 2  # center single die in middle column (0-based)
    elif count == 2:
        # Spread 2 dice in columns 1 and 3 (centered)
        col = 1 if idx == 0 else 3
    elif count == 3:
        # Spread 3 dice in columns 1,2,3
        col = 1 + idx
    elif count == 4:
        # 2x2 grid: first two dice top row, next two bottom row columns 1 and 3
        if idx < 2:
            row = 0
            col = 1 + idx * 2  # 1,3
        else:
            row = 1
            col = 1 + (idx - 2) * 2  # 1,3
    else:
        # For 5 to 10 dice:
        # top row: dice 0-4 columns 0-4
        # bottom row: dice 5-9 columns 0-4
        col = idx % 5
        row = 0 if idx < 5 else 1
    return row, col


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Multi Dice Roller")

    dice_app = DiceApp(root)
    dice_app.pack(padx=20, pady=20)


    # Example: roll 5 dice with random results
    def roll_random():
        dice_app.set_dice_count(random.randint(1, 10))
        dice_app.roll_dice(None)


    # Example: roll 3 dice with fixed results
    def roll_fixed():
        dice_app.set_dice_count(3)
        dice_app.roll_dice([3, 5, 2])


    roll_button = ctk.CTkButton(root, text="Roll Random Dice", command=roll_random)
    roll_button.pack(pady=10)

    roll_fixed_button = ctk.CTkButton(root, text="Roll 3 Fixed Dice", command=roll_fixed)
    roll_fixed_button.pack(pady=10)

    root.mainloop()
