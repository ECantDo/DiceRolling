import customtkinter as ctk

ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")

fonts = [("Arial", 16), ("Helvetica", 18, "bold")]

used_font = fonts[1]


class DiceRollerUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dice Roller Client UI Prototype :3")
        self.geometry("550x600")
        self.resizable(False, False)

        # === Top Frame: Inputs ===
        self.top_frame = ctk.CTkFrame(self, fg_color="#222222")
        self.top_frame.pack(padx=20, pady=15, fill="x")

        # Server URL
        ctk.CTkLabel(self.top_frame, text="Server URL:", anchor="w", font=used_font).pack(fill="x", pady=(5, 0))
        self.entry_url = ctk.CTkEntry(self.top_frame, font=used_font)
        self.entry_url.pack(fill="x", pady=(0, 10))
        self.entry_url.insert(0, "<Enter Provided URL>")

        # Player name
        ctk.CTkLabel(self.top_frame, text="Player Name:", anchor="w", font=used_font).pack(fill="x", pady=(5, 0))
        self.entry_player = ctk.CTkEntry(self.top_frame, font=used_font)
        self.entry_player.pack(fill="x", pady=(0, 10))

        # Dice number and sides horizontally
        dice_frame = ctk.CTkFrame(self.top_frame, fg_color="#222222")
        dice_frame.pack(fill="x", pady=(5, 10))

        ctk.CTkLabel(dice_frame, text="Number of Dice:", anchor="w", font=used_font).grid(row=0, column=0, padx=(0, 10))
        self.entry_num_dice = ctk.CTkEntry(dice_frame, width=80, font=used_font)
        self.entry_num_dice.grid(row=0, column=1, padx=(0, 20))

        ctk.CTkLabel(dice_frame, text="Sides per Dice:", anchor="w", font=used_font).grid(row=0, column=2, padx=(0, 10))
        self.entry_sides = ctk.CTkEntry(dice_frame, width=80, font=used_font)
        self.entry_sides.grid(row=0, column=3)

        # Placeholder for roll button
        self.btn_roll = ctk.CTkButton(self.top_frame, text="Roll Dice", font=used_font)
        self.btn_roll.pack(pady=(10, 15), fill="x")

        # Scrollable text box for logs/results
        self.log_text = ctk.CTkTextbox(self, width=460, height=350, font=used_font)
        self.log_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        self.log_text.configure(state="disabled")  # Readonly for now
        pass


def start_gui():
    app = DiceRollerUI()
    app.mainloop()
