from interface.frame_element import FrameElement
from tkinter import Frame, Button
from settings import THEME_COLOR
from typing import Callable
from window.generate_questions_window import GenerateQuestionsWindow


class ButtonFrame(FrameElement):
    def __init__(self, parent_frame: Frame, add_question_function: Callable, set_question_function: Callable = None):
        super().__init__(parent_frame=parent_frame, width=700, height=100, bg="white")
        self.__color_frame = Frame(self._frame, bg=THEME_COLOR, width=50, height=50)
        self.__button_frame = Frame(self._frame, bg=THEME_COLOR, width=650, height=100)
        self.__add_question = add_question_function
        self.__set_question = set_question_function

    def __place_frames(self) -> None:
        self.__color_frame.place(x=0, y=35)
        self.__button_frame.place(x=10, y=3)

    def __popup(self):
        GenerateQuestionsWindow(self._frame, add_question_function=self.__add_question).pack()

    def _pack_implementation(self) -> None:
        add_list_button = Button(self.__button_frame, text="Add Question List", command=self.__add_question)
        add_list_button.place(x=130, y=17)

        set_question_button = Button(self.__button_frame, text="Set as question", command=lambda: print())
        set_question_button.place(x=245, y=17)

        set_question_button = Button(self.__button_frame, text="Generate Questions", command=self.__popup)
        set_question_button.place(x=345, y=17)
        self.__place_frames()