import customtkinter as ctk

ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")

fonts = [("Arial", 16), ("Helvetica", 18, "bold"), ("Helvetica", 14, "bold")]

used_font = fonts[1]

MENU_BG = "#222222"  # dark gray background for dropdown
HOVER_BG = "#444444"  # lighter gray on hover


class DiceRollerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.username = None
        self.server_url = None

        self.title("Dice Roller Client UI Prototype :3")
        self.geometry("550x600")
        self.resizable(False, False)

        # Top bar frame
        top_bar = ctk.CTkFrame(self, fg_color=MENU_BG, height=40)
        top_bar.pack(fill="x", side="top")

        spacer = ctk.CTkLabel(top_bar, text="")
        spacer.pack(side="left", expand=True)

        # Hamburger button
        self.hamburger_button = ctk.CTkButton(
            top_bar,
            text="☰",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=HOVER_BG,
            font=ctk.CTkFont(size=20, weight="bold"),
            command=self.show_options_menu
        )
        self.hamburger_button.pack(side="right")

        # Create the popup menu frame but keep it hidden
        self.menu_frame = ctk.CTkFrame(self, fg_color=HOVER_BG, width=150, height=100)
        self.menu_frame.place_forget()  # hide initially

        # Add menu buttons/options inside menu_frame
        btn_set_url = ctk.CTkButton(
            self.menu_frame,
            text="Set URL",
            font=used_font,
            fg_color=HOVER_BG,
            hover_color=MENU_BG,
            border_width=0,
            corner_radius=0,
            anchor='e',
            width=120,
            height=30,
            command=self.open_url_dialog
        )
        btn_set_url.pack(fill="x", pady=0)

        btn_set_name = ctk.CTkButton(
            self.menu_frame,
            text="Set Name",
            font=used_font,
            fg_color=HOVER_BG,
            hover_color=MENU_BG,
            border_width=0,
            corner_radius=0,
            anchor='e',
            width=120,
            height=30,
            command=self.open_name_dialog
        )
        btn_set_name.pack(fill="x", pady=0)

        # === Top Frame: Inputs ===
        self.top_frame = ctk.CTkFrame(self, fg_color=MENU_BG)
        self.top_frame.pack(padx=20, pady=15, fill="x")

        # Dice number and sides horizontally
        dice_frame = ctk.CTkFrame(self.top_frame, fg_color=MENU_BG)
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

    def show_options_menu(self):
        # Toggle the menu visibility on hamburger click
        if self.menu_frame.winfo_ismapped():
            self.menu_frame.place_forget()
        else:
            # Position menu_frame under the hamburger button
            x = self.hamburger_button.winfo_rootx() - self.winfo_rootx()
            y = self.hamburger_button.winfo_rooty() - self.winfo_rooty() + self.hamburger_button.winfo_height()
            self.menu_frame.place(x=x - 85, y=y)  # Adjust x to align menu properly
            self.menu_frame.lift()

    def open_url_dialog(self):
        self.menu_frame.place_forget()
        dialog = InputDialog(self, "url")
        self.wait_window(dialog)
        if dialog.new_value:
            self.server_url = dialog.new_value
            print(self.server_url)

    def open_name_dialog(self):
        self.menu_frame.place_forget()
        dialog = InputDialog(self, "name")
        self.wait_window(dialog)
        if dialog.new_value:
            self.username = dialog.new_value
            print(self.username)


class InputDialog(ctk.CTkToplevel):
    def __init__(self, parent, selection: str):
        super().__init__(parent)
        self.new_value = None

        self.update_idletasks()  # ensure widget sizes are calculated
        # Position relative to parent window
        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()

        # Offset 50px right, 50px down from parent’s top-left
        x = parent_x + 50
        y = parent_y + 50

        self.geometry(f"400x120+{x}+{y}")

        if selection == "url":
            self.title("Set Server URL")
            ctk.CTkLabel(self, text="Enter Server URL:", font=fonts[2]).pack(pady=(10, 5))
        else:
            self.title("Set Username")
            ctk.CTkLabel(self, text="Enter Username:", font=fonts[2]).pack(pady=(10, 5))

        self.resizable(False, False)
        self.grab_set()  # make modal

        # ctk.CTkLabel(self, text="Enter Server URL:", font=fonts[2]).pack(pady=(10, 5))
        self.entry = ctk.CTkEntry(self, font=fonts[2])
        self.entry.pack(padx=20, fill="x")
        self.entry.focus()

        ctk.CTkButton(self, text="OK", command=self.on_ok, font=fonts[2]).pack(pady=15)

    def on_ok(self):
        self.new_value = self.entry.get()
        self.destroy()


def start_gui():
    app = DiceRollerUI()
    app.mainloop()
