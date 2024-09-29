from tkinter import Frame, Label
from interface.frame_element import FrameElement
from settings import THEME_COLOR
from .question_log import QuestionLog


class LeftSideFrame(FrameElement):
    def __init__(self, parent_frame: Frame, questions_logs: list[dict]):
        super().__init__(parent_frame=parent_frame, bg="white")
        self._set_packing_kwargs({"side": "left", "fill": "y"})
        self.__bottom_frame = Frame(self._frame, width=368, height=100, bg=THEME_COLOR)
        self.__question_log = QuestionLog(parent_frame=self._frame, questions_logs=questions_logs)

    def __pack_label(self) -> None:
        label = Label(self._frame, text="Question Logs", font=("Calibri", 16, "bold"), bg="white")
        label.pack(pady=(15, 5))

    def _pack_implementation(self) -> None:
        self.__pack_label()
        self.__question_log.pack()
        self.__bottom_frame.pack(pady=(3, 0))
