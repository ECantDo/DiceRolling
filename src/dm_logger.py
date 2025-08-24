import customtkinter as ctk

import requests
from queue import Queue
from requests import Response

from server_log_gui import ServerLogGUI

from server_module import get_local_time, expected_roll


class InputPassword(ctk.CTkToplevel):
    def __init__(self, parent, url: str, username: str):
        super().__init__(parent)
        self.server_url = url
        self.username = username
        self.session_token = None
        self.last_signature = None

        self.update_idletasks()

        parent_x = parent.winfo_rootx()
        parent_y = parent.winfo_rooty()
        x = parent_x + 1000
        y = parent_y + 50

        self.geometry(f"400x120+{x}+{y}")

        self.title("DM Login")
        ctk.CTkLabel(self, text="Enter Password:", font=("Helvetica", 14, "bold")).pack(pady=(10, 5))

        self.resizable(False, False)

        self.entry = ctk.CTkEntry(self, show="*", width=250)
        self.entry.pack(pady=(0, 10))
        self.entry.focus_set()

        ctk.CTkButton(self, text="Submit", command=self._on_submit).pack(pady=(0, 10))

        self.grab_set()

    def _on_submit(self):
        self._send_handshake(self.entry.get())
        self.destroy()
        pass

    def _send_handshake(self, password: str) -> bool:
        try:
            resp: Response = requests.post(
                self.server_url + "/dm-logs",
                json={"password": {
                    "password": password,
                    "username": self.username
                }},
                timeout=5,
                verify=True
            )
            resp.raise_for_status()
            data: dict = resp.json()
            self.session_token = data.get("client_token")
            self.last_signature = data.get("last_signature")
            print(f"{self.session_token = } | {self.last_signature = }")

            return True
        except Exception as e:
            return False

    def request_data(self, log_q: Queue):
        if log_q is None:
            raise Exception(f"log_q cannot be None")

        try:
            payload: dict = {"session": {
                "token": self.session_token,
                "signature": self.last_signature
            }}
            resp: Response = requests.post(
                self.server_url + "/dm-logs",
                json=payload,
                timeout=5,
                verify=True
            )
            resp.raise_for_status()
            data: dict = resp.json()

            self.last_signature = data.get("last_signature")
            for log in data.get("logs"):
                num_dice = log.get("num_dice")
                num_sides = log.get("num_sides")
                log_q.put([
                    (log.get("player"), log.get("result"), num_dice, num_sides),
                    f"{log.get("dice")}\nExpected Value: {expected_roll(num_dice, num_sides)}\n"
                    f"Timestamp: {get_local_time(log.get("timestamp"))}"
                ])
                pass
        except Exception as e:
            pass
        pass

    pass


class DMClient(ServerLogGUI):
    def __init__(self, log_q: Queue):
        super().__init__(log_q)
        self.root.title("Server Logs")
