import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

fonts = [("Arial", 16), ("Helvetica", 18, "bold"), ("Helvetica", 16, "bold")]


class LogTable(ctk.CTkFrame):
    def __init__(self, master, columns: list[str] = None, **kwargs):
        super().__init__(master, **kwargs)

        if columns is not None:
            self.columns = columns
        else:
            self.columns = ["Name", "Result", "Rolls"]

        self.rows = []

        self.scrollable_frame = ctk.CTkScrollableFrame(self, corner_radius=1)
        self.scrollable_frame.grid(row=0, column=0, sticky="nswe")
        # self.scrollable_frame.pack()
        self.grid_columnconfigure(0, weight=1)
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

    def add_row(self, row_data: tuple[str, int, int, int]):
        """
        Add a row to the log table
        Single use case currently, might change later, BUT
        :param row_data: Should be matching the column data
        FORMAT: (<name>, <total>, <number of dice>, <sides on dice>
        """
        # Shift existing rows down
        for r, (frame, labels) in enumerate(self.rows, start=1):
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

        self.rows.insert(0, (row_frame, labels))
        pass

    def clear(self):
        """
        Remove all rows from the log.
        """
        for row in self.rows:
            for widget in row:
                widget.destroy()
        self.rows.clear()
        pass


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
    root.geometry("600x400")

    log_columns = ["Name", "Result", "Rolls"]
    log_table = LogTable(root, columns=log_columns)
    log_table.pack(fill="both", expand=True, padx=10, pady=10)

    for _ in range(1):
        log_table.add_row(("Alice", 18, 1, 20))
        log_table.add_row(("Bob", 7, 2, 6))
        log_table.add_row(("Charlie", 12, 2, 8))
        log_table.add_row(("ECan", 20, 1, 20))

    root.mainloop()
    pass
