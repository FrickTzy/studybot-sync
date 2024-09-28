from tkinter import Button, Widget, Image


def toggle_pack(element: Widget, **kwargs) -> None:
    if not element.winfo_manager():
        element.pack(**kwargs)
    else:
        element.pack_forget()


def toggle_place(x: int, y: int, element: Widget) -> None:
    if not element.winfo_manager():
        element.place(x=x, y=y)
    else:
        element.place_forget()


def toggle_button_image(button: Button, first_image: Image, second_image: Image) -> None:
    """Change the button image when pressed."""
    if button.config('image')[-1] == str(first_image):
        button.config(image=second_image)
    else:
        button.config(image=first_image)
