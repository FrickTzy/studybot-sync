from tkinter import Frame, Label, Entry
from interface.editable_element import EditableElement
from helper_files import ImageManager
from custom_elements.logo_button import LogoButton
from helper_files import FunctionManager
from typing import Callable


class QuestionElement(EditableElement):
    __BACKGROUND = "lightgray"

    def __init__(self, parent_frame: Frame,
                 image_manager: ImageManager, function_manager: FunctionManager, remove_function: Callable,
                 initial_question: str = "", initial_answer: str = ""):
        super().__init__(parent_frame, bg=self.__BACKGROUND, width=528, height=41)
        self.__image_manager = image_manager

        self.__question_entry = self.__get_question_entry()
        self.__question_entry.insert(0, initial_question)

        self.__answer_entry = self.__get_answer_entry()
        self.__answer_entry.insert(0, initial_answer)

        self.__question_label = self.__get_question_label()
        self.__answer_label = self.__get_answer_label()

        self.__remove_button = self.__get_remove_button(function=remove_function)

    def __get_question_label(self) -> Label:
        return Label(self._frame, font=("Calibri", 11, "bold"), text="Question:", bg="lightgray")

    def __get_question_entry(self) -> Entry:
        return Entry(self._frame, width=22, font=("Calibri", 11))

    def __get_answer_label(self) -> Label:
        return Label(self._frame, font=("Calibri", 11, "bold"), text="Answer:", bg="lightgray")

    def __get_answer_entry(self) -> Entry:
        return Entry(self._frame, width=22, font=("Calibri", 11))

    def __get_remove_button(self, function: Callable) -> LogoButton:
        def button_function() -> None:
            if function(question=self):
                self._frame.destroy()
        remove_image = self.__image_manager.get_tkinter_image(name="trash_can_logo.png", size=(25, 25))
        self._frame.remove_image = remove_image
        remove_button = LogoButton(self._frame, image=remove_image, command=button_function,
                                   background=self.__BACKGROUND)
        return remove_button

    @property
    def get_question(self) -> str:
        return self.__question_entry.get()

    @property
    def get_answer(self) -> str:
        return self.__answer_entry.get()

    def _base_pack(self) -> None:
        self._pack()
        self.__question_label.place(x=12, y=8)
        self.__question_entry.place(x=85, y=8)
        self.__answer_label.place(x=255, y=8)
        self.__answer_entry.place(x=320, y=8)

    def pack_view(self) -> None:
        self._base_pack()
        self.__answer_entry.config(state="readonly")
        self.__question_entry.config(state="readonly")

    def pack_edit(self) -> None:
        self._base_pack()
        self.__answer_entry.config(state="normal")
        self.__question_entry.config(state="normal")
        self.__remove_button.place(x=490, y=6)

    @property
    def shown(self) -> bool:
        return bool(self._frame.winfo_manager())

    def unpack(self) -> None:
        self._unpack()
        self.__question_label.place_forget()
        self.__question_entry.place_forget()
        self.__answer_label.place_forget()
        self.__answer_entry.place_forget()
        self.__remove_button.place_forget()

