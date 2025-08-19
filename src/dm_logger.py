import customtkinter as ctk


class InputPassword(ctk.CTkToplevel):
    def __init__(self, parent, url: str):
        super().__init__(parent)
        self.password = None
        self.server_url = url

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
        self.password = self.entry.get()
        self.destroy()
        pass

    pass


class DMClient:

    def __init__(self, url: str):
        pass

    def send_handshake(self, password: str, ):
        pass
