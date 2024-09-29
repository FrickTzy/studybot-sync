from tkinter import Frame, Canvas
from interface.frame_element import FrameElement
from .log_element import LogElement


class QuestionLog(FrameElement):
    def __init__(self, parent_frame: Frame, questions_logs: list[dict]):
        super().__init__(parent_frame=parent_frame)

        question_list_canvas = Canvas(self._frame, width=348, height=430, highlightthickness=0)
        question_log_frame = Frame(question_list_canvas, width=348, height=430)

        question_list_canvas.create_window((0, 0), window=question_log_frame, anchor="nw")
        question_list_canvas.pack()

        self._set_packing_kwargs(packing_kwargs={"padx": (15, 5), "pady": (10, 12)})

        self.__log_list = [LogElement(question_log_frame, question_log) for question_log in questions_logs]

    def _pack_implementation(self) -> None:
        for log in self.__log_list:
            log.pack()
