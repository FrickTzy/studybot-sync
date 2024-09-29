from tkinter import Frame, Label
from interface import FrameElement


class LogElement(FrameElement):
    __BACKGROUND = "lightgray"

    def __init__(self, parent_frame: Frame, question_log: dict):
        super().__init__(parent_frame, bg=self.__BACKGROUND, width=328, height=42)
        self._set_packing_kwargs(packing_kwargs={"padx": 10, "pady": (10, 0)})
        self.__question_name_label = self.__get_label(text=question_log["questionName"], size=11)
        self.__time_label = self.__get_label(text=question_log["time"])
        self.__date_label = self.__get_label(text=question_log["date"])
        self.__score_label = self.__get_label(text=question_log["score"])

    def __get_label(self, text: str, size: int = 10) -> Label:
        return Label(self._frame, font=("Calibri", size, "bold"), text=text, bg="lightgray")

    def _pack_implementation(self) -> None:
        self.__question_name_label.place(x=5, y=0)
        self.__time_label.place(x=265, y=17)
        self.__date_label.place(x=263, y=2)
        self.__score_label.place(x=5, y=17)
