from tkinter import Entry, END


def add_placeholder_to_frame(entry: Entry, placeholder_text: str, placeholder_text_color: str = "grey",
                             normal_text_color: str = "black") -> None:
    """ Adds placeholder text to the entry widget. """
    entry.insert(0, placeholder_text)
    entry.config(fg=placeholder_text_color)

    def on_focus_in(event) -> None:
        if entry.get() == placeholder_text:
            entry.delete(0, END)
            entry.config(fg=normal_text_color)

    def on_focus_out(event) -> None:
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg=placeholder_text_color)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)