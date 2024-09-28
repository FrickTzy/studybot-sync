from tkinter import Frame, Label, END, Listbox
from interface.frame_element import FrameElement
from settings import THEME_COLOR


class LeftSideFrame(FrameElement):
    def __init__(self, parent_frame: Frame, questions_logs: list[dict]):
        super().__init__(parent_frame=parent_frame, bg="white", width=600)
        self._set_packing_kwargs({"side": "left", "fill": "y"})
        self.__bottom_frame = Frame(self._frame, width=368, height=100, bg=THEME_COLOR)
        self.__history_listbox = Listbox(self._frame, width=58, height=27, bg="SystemButtonFace", highlightthickness=0,
                                         bd=0)

        for question_log in questions_logs:
            self.__history_listbox.insert(END, f"{question_log['questionsAmount']}: {question_log['correctAnswers']}")

    def __pack_label(self) -> None:
        label = Label(self._frame, text="Question Logs", font=("Calibri", 16, "bold"), bg="white")
        label.pack(pady=(15, 5))

    def __pack_listbox(self) -> None:
        self.__history_listbox.pack(padx=(15, 5), pady=10)

    def _pack_implementation(self) -> None:
        self.__pack_label()
        self.__pack_listbox()
        self.__bottom_frame.pack(side="bottom", pady=(3, 0))