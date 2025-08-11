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
        elif 1 <= result <= 6:
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


class DiceApp(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    pass


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Simple Dice Roller")

    dice_paths = [f"assets/d6/dice{i}.png" for i in range(1, 7)]  # Your renamed dice images here
    dice_frame = SingleDiceRollerFrame(root, dice_paths)
    dice_frame.pack(padx=20, pady=20)

    roll_button = ctk.CTkButton(root, text="Roll Dice", command=lambda: dice_frame.roll(None))
    roll_button.pack(pady=10)

    root.mainloop()
