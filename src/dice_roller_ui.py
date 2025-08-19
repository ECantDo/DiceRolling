import customtkinter as ctk
import requests

from dice_logic import roll_dice
from settings_manager import SettingsManager
from script_updater import CURRENT_VERSION
from dice_animation import DiceApp
from dm_logger import InputPassword

ctk.set_appearance_mode("dark")  # "dark" or "light"
ctk.set_default_color_theme("blue")

fonts = [("Arial", 16), ("Helvetica", 18, "bold"), ("Helvetica", 14, "bold")]

used_font = fonts[1]

MENU_BG = "#222222"  # dark gray background for dropdown
HOVER_BG = "#444444"  # lighter gray on hover


# TODO:
#   - DM logs


class DiceRollerUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.settings = SettingsManager()

        self.username = self.settings.get("username", None)
        self.server_url = self.settings.get("server_url", None)
        self.logs: list[tuple[str, bool]] = []

        self.title("Dice Roller Client UI Prototype :3")
        self.geometry("1350x600")
        self.resizable(False, False)

        main_content_frame = ctk.CTkFrame(self, width=500, fg_color=MENU_BG)

        # Top bar frame
        top_bar = ctk.CTkFrame(self, fg_color=MENU_BG, height=40)
        top_bar.pack(fill="x", side="top")

        # spacer = ctk.CTkLabel(top_bar, text="")
        # spacer.pack(side="left", expand=True)

        # Version Number
        version_number = ctk.CTkLabel(
            top_bar,
            text=f"V {CURRENT_VERSION}",
            font=("impact", 20, "bold"),
            text_color="#5F5F5F"
        )
        version_number.pack(side="left", padx=(10, 5))
        # Hamburger button

        self._setup_menu_button(top_bar)

        # === Top Frame: Inputs ===
        self.top_frame = ctk.CTkFrame(main_content_frame, fg_color=MENU_BG)
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
        self.btn_roll = ctk.CTkButton(self.top_frame, text="Roll Dice", font=used_font,
                                      command=self.perform_roll
                                      )
        self.btn_roll.pack(pady=(10, 15), fill="x")

        # Scrollable text box for logs/results
        self.log_text = ctk.CTkTextbox(main_content_frame, width=460, height=350, font=used_font)
        self.log_text.pack(side="left", fill="both", expand=True)
        self.log_text.configure(state="disabled")  # Readonly for now

        main_content_frame.pack(side="left", padx=(10, 0), pady=5, fill="both", expand=True)

        self.dice_app = DiceApp(self)
        self.dice_app.pack(side="right", fill='none', anchor="center", padx=10, pady=5)

        self.after(200, self.startup_dialogs)
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
        dialog = InputDialog(self, "url", self.server_url)
        self.wait_window(dialog)

        self.server_url = dialog.new_value
        if (self.server_url is not None and (len(self.server_url) != 0)) and (not self.server_url.endswith("/roll")):
            self.server_url = self.server_url.rstrip("/")

    def open_name_dialog(self):
        self.menu_frame.place_forget()
        dialog = InputDialog(self, "name", self.username)
        self.wait_window(dialog)
        if dialog.new_value:
            self.username = dialog.new_value
            if self.username:
                self.settings.set("username", self.username)

    def startup_dialogs(self):
        if not self.settings.get("skip_fetch_url", False):
            # Open URL dialog first
            self.open_url_dialog()
        # After URL dialog closes, check username
        if not self.username:
            self.open_name_dialog()

    def open_dm_portal(self):
        self.menu_frame.place_forget()
        dialog = InputPassword(self, self.server_url)
        self.wait_window(dialog)
        password: str = dialog.password
        print(f"{password = }")
        # TODO: Finish function
        pass

    def perform_roll(self):
        dice = None

        def v_roll():
            if sides in (4, 6, 8, 10, 12, 20) and dice:
                self.dice_app.set_dice_count(len(dice))
                self.dice_app.roll_dice(dice, sides)
                pass
            else:
                self.dice_app.set_dice_count(0)

        try:
            num_dice = int(self.entry_num_dice.get())
            sides = int(self.entry_sides.get())
        except ValueError:
            self.append_log("Please enter valid numbers for dice and sides.", error=True)
            return

        if not self.server_url:
            # Local roll
            dice, total = roll_dice(num_dice, sides)
            if dice is None:
                self.append_log(f"Local roll: Total: {total} | {num_dice}d{sides}")
            else:
                v_roll()
                self.append_log(f"Local roll: Total: {total} | {num_dice}d{sides} | Dice: {dice}")
        else:
            if num_dice > 1000 and sides > 1000:
                return
            payload = {
                "player": self.username,
                "num_dice": num_dice,
                "num_sides": sides,
                "version": CURRENT_VERSION
            }
            try:
                # Timeout is in seconds
                resp = requests.post(self.server_url + "/roll", json=payload, timeout=5,
                                     verify=False)
                resp.raise_for_status()
                data: dict = resp.json()

                error = data.get("error", "")
                if error:
                    self.append_log(f"Error: {data['error']}", error=True)
                else:
                    dice = data["dice"]
                    if dice is None:
                        self.dice_app.set_dice_count(0)
                        self.append_log(f"Total: {data['result']} | {num_dice}d{sides}")
                    else:
                        v_roll()
                        self.append_log(f"Total: {data['result']} | {num_dice}d{sides} | Dice: {dice} ")

            except Exception as e:
                self.append_log(f"Error contacting server: {e}", error=True)
                return

        pass

    def append_log(self, text, error=False):
        self.log_text.configure(state="normal")
        self.logs.insert(0, (text, error))
        self.logs = self.logs[:18]  # Only keep the last 18? -> Remove if want more

        # Clear all text first
        self.log_text.delete("1.0", "end")

        # Rebuild text with coloring
        for i, (line_text, is_error) in enumerate(self.logs):
            self.log_text.insert(f"{i + 1}.0", line_text + "\n")
            if is_error:
                # Tag line with red foreground, approximate line range
                start = f"{i + 1}.0"
                end = f"{i + 1}.end"
                self.log_text.tag_add("error", start, end)

        # Configure tag style here or once during init
        self.log_text.tag_config("error", foreground="red")

        self.log_text.configure(state="disabled")
        pass

    def _setup_menu_button(self, top_bar):
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

        btn_open_logs = ctk.CTkButton(
            self.menu_frame,
            text="DM Logs",
            font=used_font,
            fg_color=HOVER_BG,
            hover_color=MENU_BG,
            border_width=0,
            corner_radius=0,
            anchor='e',
            width=120, height=30,
            command=self.open_dm_portal
        )
        btn_open_logs.pack(fill='x', pady=0)
        pass

    pass


class InputDialog(ctk.CTkToplevel):
    def __init__(self, parent, selection: str, current_value: str | None):
        super().__init__(parent)
        self.new_value = None

        if current_value is None:
            current_value = ""

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

        self.entry = ctk.CTkEntry(self, font=fonts[2])
        self.entry.pack(padx=20, fill="x")
        self.entry.insert(0, current_value)
        self.entry.focus()

        ctk.CTkButton(self, text="OK", command=self.on_ok, font=fonts[2]).pack(pady=15)

    def on_ok(self):
        self.new_value = self.entry.get()
        self.destroy()


def start_gui():
    app = DiceRollerUI()
    app.mainloop()
