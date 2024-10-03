from tkinter import Frame, Label, Entry
from interface.editable_element import EditableElement
from helper_files import ImageManager
from custom_elements.logo_button import LogoButton
from typing import Callable
from collections import defaultdict


class QuestionElement(EditableElement):
    __BACKGROUND = "lightgray"

    def __init__(self, parent_frame: Frame,
                 image_manager: ImageManager, remove_function: Callable,
                 data_dict: defaultdict):
        super().__init__(parent_frame, bg=self.__BACKGROUND, width=528, height=41)
        self.__image_manager = image_manager
        self.__data_dict = data_dict

        self.__question_entry = self.__get_question_entry()
        self.__question_entry.insert(0, data_dict["question"])

        self.__answer_entry = self.__get_answer_entry()
        self.__answer_entry.insert(0, data_dict["answer"])

        self.__question_label = self.__get_question_label()
        self.__answer_label = self.__get_answer_label()

        self.__remove_function = remove_function

        self.__remove_button = self.__get_remove_button()

        self.__data_dict = data_dict

    def __get_question_label(self) -> Label:
        return Label(self._frame, font=("Calibri", 11, "bold"), text="Question:", bg="lightgray")

    def __get_question_entry(self) -> Entry:
        return Entry(self._frame, width=22, font=("Calibri", 11))

    def __get_answer_label(self) -> Label:
        return Label(self._frame, font=("Calibri", 11, "bold"), text="Answer:", bg="lightgray")

    def __get_answer_entry(self) -> Entry:
        return Entry(self._frame, width=22, font=("Calibri", 11))

    def __get_remove_button(self) -> LogoButton:
        remove_image = self.__image_manager.get_tkinter_image(name="trash_can_logo.png", size=(25, 25))
        self._frame.remove_image = remove_image
        remove_button = LogoButton(self._frame, image=remove_image, command=self.delete_question,
                                   background=self.__BACKGROUND)
        return remove_button

    def delete_question(self) -> None:
        if self.__remove_function(question=self):
            self._frame.destroy()

    def save_data(self) -> None:
        self.__data_dict["answer"] = self.__answer_entry.get()
        self.__data_dict["question"] = self.__question_entry.get()

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

    def unpack(self) -> None:
        self._unpack()
        self.__question_label.place_forget()
        self.__question_entry.place_forget()
        self.__answer_label.place_forget()
        self.__answer_entry.place_forget()
        self.__remove_button.place_forget()

    @property
    def empty_input(self) -> bool:
        return (not self.__question_entry.get()) and (not self.__answer_entry.get())

    @property
    def data_dict(self) -> defaultdict:
        return self.__data_dict

