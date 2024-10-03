from tkinter import Frame
from interface.frame_element import FrameElement
from frame.right.question_list.question_title.questions_title_element import QuestionTitleElement
from .question_frame import QuestionFrame
from helper_files import ImageManager
from helper_files.state_manager.element_state import ElementState
from helper_files.state_manager.state_manager import StateManager
from helper_files.question_data_manager import delete_question
from helper_files import FunctionManager, ToggleStateManager, UploadManager
from utils.generate_functions import generate_choices
from typing import Callable
from threading import Thread
from copy import copy
from collections import defaultdict


class QuestionMainFrame(FrameElement):
    __PADDING_X = 10
    __PADDING_Y = 10

    def __init__(self, question: dict, parent_frame: Frame,
                 image_manager: ImageManager, state_manager: StateManager, parent_upload_function: Callable,
                 parent_delete_function: Callable):
        super().__init__(parent_frame=parent_frame)
        self.__state_manager = state_manager
        self.__image_manager = image_manager

        self.__main_question_dict = question
        self.__data_manager: list[defaultdict] = []

        toggled_on = self.__state_manager.on_editing_mode()
        self.__toggle_state_manager = ToggleStateManager(toggled_on=toggled_on)
        self.__upload_manager = UploadManager()

        self.__function_manager = FunctionManager()

        self.__add_functions(upload_function=parent_upload_function, delete_function=parent_delete_function)

        self._set_packing_kwargs(packing_kwargs={"padx": self.__PADDING_X, "pady": self.__PADDING_Y})
        self.__question_frame = QuestionFrame(parent_frame=self._frame, question_list=question.get("questions"),
                                              image_manager=image_manager, state_manager=self.__state_manager,
                                              function_manager=self.__function_manager,
                                              toggle_state_manager=self.__toggle_state_manager,
                                              data_manager=self.__data_manager)
        self.__title_element = QuestionTitleElement(parent_frame=self._frame, initial_title=question.get("title"),
                                                    image_manager=image_manager, state_manager=self.__state_manager,
                                                    function_manager=self.__function_manager,
                                                    toggled_on=toggled_on, upload_manager=self.__upload_manager)

    def __add_functions(self, upload_function: Callable, delete_function: Callable):
        self.__function_manager.add_function("save_question", self.__save_function)
        self.__function_manager.add_function("set_view", self.__set_view)
        self.__function_manager.add_function("delete_question", lambda: delete_function(self))
        self.__function_manager.add_function("delete_question", self.__delete_question)
        self.__function_manager.add_function("set_edit", self.__set_edit)
        self.__function_manager.add_function("revert_question", self.__revert_function)
        self.__function_manager.add_function("toggle_function", self.__toggle_state_manager.toggle)
        self.__function_manager.add_function("upload_function", lambda: upload_function(self,
                                                                                        self.__main_question_dict))

    def __revert_function(self) -> None:
        if not self.__main_question_dict.get("title"):
            self.__delete_question()
        else:
            self.__question_frame.set_questions(question_list=self.__main_question_dict["questions"],
                                                image_manager=self.__image_manager)
            self.__title_element.set_title(title=self.__main_question_dict["title"])
            self.__function_manager.call_functions("set_view")

    def __save_function(self) -> None:
        def check_if_add_choices() -> None:
            question_dict_list = self.__main_question_dict["questions"]
            if not all(question_dict["question"] and question_dict["answer"] for question_dict in question_dict_list):
                return
            if all("choices" in question_dict for question_dict in question_dict_list):
                return
            question_dict_list_with_choices = generate_choices(question_dict_list=question_dict_list)
            if not question_dict_list_with_choices:
                return
            self.__main_question_dict["questions"] = question_dict_list_with_choices
            self.__data_manager = question_dict_list_with_choices

        self.__question_frame.save_data()

        self.__main_question_dict["questions"] = copy(self.__data_manager)
        self.__main_question_dict["title"] = self.__title_element.get_title

        self.__function_manager.call_functions("set_view")

        if self.__main_question_dict["questions"]:
            Thread(target=check_if_add_choices, daemon=True).start()

    def __delete_question(self) -> None:
        self._frame.destroy()
        delete_question(question=self.__main_question_dict)

    def _pack_implementation(self) -> None:
        self.__upload_manager.uploaded = self.__main_question_dict["questionUploaded"]
        self.__title_element.pack()
        self.__question_frame.pack()

    def unpack(self) -> None:
        self._frame.pack_forget()
        self.__title_element.unpack()
        self.__question_frame.unpack()

    def __update(self) -> None:
        self.__title_element.unpack()
        self.__question_frame.unpack()
        self._pack_implementation()

    def __set_edit(self) -> None:
        self.__state_manager.state = ElementState.EDIT
        self.__update()

    def __set_view(self) -> None:
        self.__state_manager.state = ElementState.VIEW
        self.__update()

