from tkinter import messagebox, Tk, Toplevel


def show_notification():
    messagebox.showinfo("Notification", "This is a pop-up notification!")


def resize_window(window: Tk, window_size: tuple[int, int]) -> None:
    width, height = window_size
    window.geometry(f'{width}x{height}')


def center_window(window: Tk | Toplevel, window_size: tuple[int, int]) -> None:
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    width, height = window_size

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f'{width}x{height}+{x}+{y}')