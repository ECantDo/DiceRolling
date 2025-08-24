import customtkinter as ctk
from logger_ui import LogTable  # import your LogTable class here


class ServerLogGUI:

    def __init__(self, log_q):
        self.log_q = log_q
        self.root = ctk.CTk()
        self.root.title("Dice Roller Server")

        self._on_close = None

    def set_on_close(self, callback):
        self._on_close = callback

    def gui_main(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root.geometry("1000x400")

        log_columns = ["Name", "Result", "Rolls"]
        log_table = LogTable(self.root, columns=log_columns)
        log_table.pack(fill="both", expand=True, padx=10, pady=10)

        def poll_queue():
            while not self.log_q.empty():
                row_data = self.log_q.get()
                log_table.add_row(*row_data)
            self.root.after(100, poll_queue)

        def on_close():
            if self._on_close:
                self._on_close()
            self.root.destroy()

        self.root.protocol("WM_DELETE_WINDOW", on_close)

        poll_queue()
        self.root.mainloop()
