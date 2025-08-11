import random
import customtkinter as ctk
from PIL import Image
from PIL import ImageTk


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


# For later use when adding more dice
__dice_face_indexing: tuple[int, int, int, int, int, int] = (4, 6, 8, 10, 12, 20)


class DiceApp(ctk.CTkFrame):
    def __init__(self, master, max_dice: int = 10, **kwargs):
        super().__init__(master, **kwargs)
        self.max_dice = max_dice
        self.container_width = 700
        self.container_height = 300

        # Load all images
        self.dice_frames = [ImageTk.PhotoImage(Image.open(path).resize((128, 128))) for path in
                            [f"assets/d6/dice{i}.png" for i in range(1, 7)]
                            ]

        # Make the frame
        self.dice_container = ctk.CTkFrame(self, width=self.container_width, height=self.container_height)
        self.dice_container.pack(pady=10)
        self.dice_container.pack_propagate(False)  # Fix size, don’t shrink to contents

        self.dice_widgets: list[SingleDiceRollerFrame] = []
        # Init empty
        self.create_dice_widgets(0)
        pass

    def create_dice_widgets(self, count: int):
        # Clamp the range
        count: int = max(0, min(count, self.max_dice))

        if count == len(self.dice_widgets):
            return  # Already have the correct number; don't need to remake

        # Clear old dice
        for die in self.dice_widgets:
            die.destroy()
        self.dice_widgets.clear()

        # Create new dice
        for _ in range(count):
            die = SingleDiceRollerFrame(self.dice_container, self.dice_frames)
            die.pack(side="left", padx=5)
            self.dice_widgets.append(die)

        pass

    def set_dice_count(self, count: int):
        self.create_dice_widgets(count)
        pass

    def roll_dice(self, results: list[int] | None):
        """
        Roll all the dice with either a random outcome, or a pre-set outcome
        :param results: If None; will make all dice that exist roll randomly, otherwise, the dice will be remade, then
        rolled with the expected outcomes
        :return:
        """
        if results is None:
            results = [None] * len(self.dice_widgets)
        elif len(results) != len(self.dice_widgets):
            return

        for i, die in enumerate(self.dice_widgets):
            die.roll(results[i])
        pass

    pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Multi Dice Roller")

    dice_app = DiceApp(root)
    dice_app.pack(padx=20, pady=20)


    # Example: roll 5 dice with random results
    def roll_random():
        dice_app.set_dice_count(5)
        dice_app.roll_dice(None)


    # Example: roll 3 dice with fixed results
    def roll_fixed():
        dice_app.set_dice_count(3)
        dice_app.roll_dice([3, 5, 2])


    roll_button = ctk.CTkButton(root, text="Roll 5 Random Dice", command=roll_random)
    roll_button.pack(pady=10)

    roll_fixed_button = ctk.CTkButton(root, text="Roll 3 Fixed Dice", command=roll_fixed)
    roll_fixed_button.pack(pady=10)

    root.mainloop()
