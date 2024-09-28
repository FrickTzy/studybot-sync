from tkinter import Frame, Label
from interface.frame_element import FrameElement


class HeaderFrame(FrameElement):
    def __init__(self, parent_frame: Frame, title: str):
        super().__init__(parent_frame=parent_frame, bg="#eb9d02", height=50)
        self._set_packing_kwargs({"fill": "x"})
        self.__title = title

    def _pack_implementation(self) -> None:
        header_label = Label(self._frame, text=self.__title, bg="#eb9d02", fg="white", font=("Calibri", 20, "bold"))
        header_label.pack(pady=10)