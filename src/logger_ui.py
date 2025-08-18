import customtkinter as ctk
from functools import partial

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

fonts = [("Arial", 16), ("Helvetica", 18, "bold"), ("Helvetica", 16, "bold")]


class LogTable(ctk.CTkFrame):
    def __init__(self, master, columns: list[str] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_row_click = self.on_row_click

        if columns is not None:
            self.columns = columns
        else:
            self.columns = ["Name", "Result", "Rolls"]

        self.rows = []

        # Scrolling
        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=1, width=200)
        self.scrollable_frame.grid(row=0, column=0, sticky="nswe")

        # NOTES
        self.notes_panel = ctk.CTkTextbox(self, state="disabled", wrap="word", font=fonts[2], width=250)
        self.notes_panel.grid(row=0, column=1, sticky="nswe")

        # Configure grid to split space between log and notes
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Headers
        for col_idx, col_name in enumerate(columns):
            label = ctk.CTkLabel(self.scrollable_frame, text=col_name, anchor='w', font=fonts[1])
            label.grid(row=0, column=col_idx, sticky='w', padx=(5, 10))
            self.scrollable_frame.grid_columnconfigure(col_idx, weight=1, uniform="col")
            # self.scrollable_frame.grid_columnconfigure(col_idx, minsize=150, uniform="col")

            pass

        # Make columns expand evenly
        for i in range(len(columns)):
            self.grid_columnconfigure(i, weight=1)
        pass

    def add_row(self, row_data: tuple[str, int, int, int], notes: str = None):
        """
        Add a row to the log table
        Single use case currently, might change later, BUT
        :param row_data: Should be matching the column data
         FORMAT: (<name>, <total>, <number of dice>, <sides on dice>
        :param notes: Any additional notes that should be displayed

        """
        # Shift existing rows down
        for r, (frame, labels, note) in enumerate(self.rows, start=1):
            frame.grid_configure(row=r + 1)

        color = get_color_for_roll(*row_data[1:])

        # Create a frame for each row
        row_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color=color,
            corner_radius=0
        )
        row_frame.grid(
            row=1, column=0,
            columnspan=len(self.columns),
            sticky='ew',
            padx=5, pady=0
        )
        self.grid_columnconfigure(0, weight=1)  # Make column 0 expandable

        labels = []
        data = list(row_data[:-1])
        data[-1] = f"{data[-1]}d{row_data[-1]}"

        for col_idx, cell_data in enumerate(data):
            label = ctk.CTkLabel(
                row_frame,
                text=str(cell_data),
                anchor="w",
                font=fonts[2],
                fg_color="transparent"
            )
            label.grid(row=0, column=col_idx, sticky="e", padx=(5, 15))
            labels.append(label)

        for i in range(len(self.columns)):
            row_frame.grid_columnconfigure(i, weight=1, uniform="col")

        def on_click(event, row_index=len(self.rows)):

            row_index = len(self.rows) - row_index - 1
            # Remove outline from previously selected row

            for old_frame, _, _ in self.rows:
                old_frame.configure(border_width=0)

            # Add outline to newly selected row
            frame, _, _ = self.rows[row_index]
            frame.configure(border_width=2, border_color="#3498db")  # blue outline

            # Update notes panel
            notes = self.rows[row_index][2]

            if notes:
                self.notes_panel.configure(state="normal")
                self.notes_panel.delete("1.0", "end")
                self.notes_panel.insert("1.0", notes)
                self.notes_panel.configure(state="disabled")
            else:
                self.notes_panel.configure(state="normal")
                self.notes_panel.delete("1.0", "end")
                self.notes_panel.configure(state="disabled")

            if self.on_row_click:
                self.on_row_click(row_index)

        row_frame.bind("<Button-1>", on_click)
        for label in labels:
            label.bind("<Button-1>", on_click)

        # Insert it :)
        self.rows.insert(0, (row_frame, labels, notes))
        pass

    def on_row_click(self, row_index):
        _, _, note_text = self.rows[row_index]
        if note_text:
            self.notes_panel.configure(state="normal")
            self.notes_panel.delete("1.0", "end")
            self.notes_panel.insert("1.0", note_text)
            self.notes_panel.configure(state="disabled")
        else:
            self.notes_panel.configure(state="normal")
            self.notes_panel.delete("1.0", "end")
            self.notes_panel.configure(state="disabled")

    def clear(self):
        """
        Remove all rows from the log.
        """
        for row in self.rows:
            for widget in row:
                widget.destroy()
        self.rows.clear()
        pass

    # def _refresh_row_positions(self, skip=None):
    #     # Re-grid all rows accounting for notes row at 'skip' grid row
    #     row_num = 1
    #     for (frame, labels, note) in self.rows:
    #         if skip is not None and row_num >= skip:
    #             row_num += 1  # leave a gap for notes row
    #         frame.grid_configure(row=row_num)
    #         for label in labels:
    #             label.grid_configure(row=0)
    #         row_num += 1


def get_default_color() -> str:
    return "#34495e"


def get_color_for_roll(total: int | str, num_dice: int | str, num_sides: int | str) -> str:
    """
    Determine the background color based on the roll
    :param total: Total rolled value
    :param num_dice: Numer of dice rolled
    :param num_sides: Number of sides per dice
    :return: Returns a hex string for the color
    """
    try:
        total = int(total)
        num_sides = int(num_sides)
        num_dice = int(num_dice)
    except ValueError:
        return get_default_color()

    if num_dice == 1 and num_sides == 20:
        if total == 1:
            return "#e74c3c"  # Critical failure : red
        if total == 20:
            return "#2ecc71"  # Critical success : green
        pass

    return get_default_color()

    pass


if __name__ == "__main__":
    root = ctk.CTk()
    root.title("Dice Roll Log")
    root.geometry("1000x500")

    log_columns = ["Name", "Result", "Rolls"]
    log_table = LogTable(root, columns=log_columns)
    log_table.pack(fill="both", expand=True, padx=10, pady=10)

    for _ in range(1):
        log_table.add_row(("Alice", 18, 1, 20), notes="Hello")
        log_table.add_row(("Bob", 7, 2, 6), "TESTING")
        log_table.add_row(("Charlie", 12, 2, 8), "AHEHIA")
        log_table.add_row(("ECan", 20, 1, 20), "EEEEE")

    root.mainloop()
    pass
