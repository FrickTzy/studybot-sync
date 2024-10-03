from interface.editable_element import EditableElement
from tkinter import Frame
from helper_files import ImageManager
from .question_element import QuestionElement
from settings import MARGIN_BETWEEN_QUESTION
from helper_files import StateManager
from helper_files import FunctionManager
from helper_files import ToggleStateManager
from collections import defaultdict


class QuestionFrame(EditableElement):
    def __init__(self, question_list: list[dict], parent_frame: Frame, function_manager: FunctionManager,
                 image_manager: ImageManager, state_manager: StateManager, toggle_state_manager: ToggleStateManager,
                 data_manager: list[defaultdict]):
        super().__init__(parent_frame, bg="lightgray")
        self.__question_element_list: list[QuestionElement] = []
        self.__data_manager: list[defaultdict] = data_manager
        self.__state_manager = state_manager
        self.__toggle_state_manager = toggle_state_manager
        self.add_functions(function_manager=function_manager, image_manager=image_manager)
        if question_list:
            self.set_questions(question_list=question_list, image_manager=image_manager)
        else:
            self.__set_question(image_manager=image_manager)

    def add_functions(self, function_manager: FunctionManager, image_manager: ImageManager) -> None:
        function_manager.add_function("toggle_function", self.__toggle_function)
        function_manager.add_function("add_question", lambda: self.__set_question(image_manager=image_manager))
        function_manager.add_function("add_question", lambda: function_manager.call_functions("set_edit"))

    def set_questions(self, question_list: list[dict], image_manager: ImageManager) -> None:
        self.unpack()
        self.__question_element_list.clear()
        self.__data_manager.clear()
        for question_dict in question_list:
            self.__set_question(image_manager=image_manager, question_dict=question_dict)

    def __set_question(self, image_manager: ImageManager, question_dict: dict = None) -> None:
        data_dict = defaultdict(lambda: "")
        if question_dict:
            data_dict.update(question_dict)
        question_element = QuestionElement(image_manager=image_manager,
                                           parent_frame=self._frame,
                                           remove_function=self.__check_if_can_remove_question, data_dict=data_dict)
        self.__question_element_list.append(question_element)
        self.__data_manager.append(data_dict)

    def save_data(self) -> None:
        only_one_question = len(self.__question_element_list) == 1
        for question_element in self.__question_element_list:
            if question_element.empty_input and not only_one_question:
                question_element.delete_question()
            else:
                question_element.save_data()

    @property
    def get_all_question_dict(self) -> list[dict]:
        return self.__data_manager

    def __check_if_can_remove_question(self, question: QuestionElement) -> bool:
        if len(self.__question_element_list) == 1:
            return False
        self.__question_element_list.remove(question)
        self.__data_manager.remove(question.data_dict)
        return True

    def __toggle_function(self) -> None:
        if not self._frame.winfo_manager():
            self.pack()
        else:
            self.unpack()

    def pack(self) -> None:
        if not self.__toggle_state_manager.toggled_on:
            return
        if self.__state_manager.on_editing_mode():
            self.pack_edit()
        else:
            self.pack_view()

    def _base_pack(self) -> None:
        self._pack(padx=(MARGIN_BETWEEN_QUESTION, 0), pady=5)

    def pack_view(self) -> None:
        self._base_pack()
        for question_element in self.__question_element_list:
            question_element.pack_view()

    def pack_edit(self) -> None:
        self._base_pack()
        for question_element in self.__question_element_list:
            question_element.pack_edit()

    def unpack(self) -> None:
        self._unpack()
        for question_element in self.__question_element_list:
            question_element.unpack()




