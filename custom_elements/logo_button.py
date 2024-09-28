from tkinter import Button, Frame, Image
from typing import Callable


class LogoButton(Button):
    def __init__(self, parent_frame: Frame, image: Image, command: Callable, background: str):
        super().__init__(parent_frame, image=image, command=command, bd=0, activebackground=background, bg=background)