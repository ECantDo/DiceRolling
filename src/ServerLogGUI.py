import customtkinter as ctk
from LoggerUI import LogTable  # import your LogTable class here


class ServerLogGUI:

    def __init__(self, log_q):
        self.log_q = log_q

    def gui_main(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        root = ctk.CTk()
        root.title("Dice Roller Server")
        root.geometry("1000x400")

        log_columns = ["Name", "Result", "Rolls"]
        log_table = LogTable(root, columns=log_columns)
        log_table.pack(fill="both", expand=True, padx=10, pady=10)

        def poll_queue():
            while not self.log_q.empty():
                row_data = self.log_q.get()
                log_table.add_row(*row_data)
            root.after(100, poll_queue)

        poll_queue()
        root.mainloop()
