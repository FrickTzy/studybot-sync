from interface.editable_element import EditableElement
from tkinter import Frame
from helper_files import ImageManager
from .question_element import QuestionElement
from settings import MARGIN_BETWEEN_QUESTION
from helper_files import StateManager
from helper_files import FunctionManager
from helper_files import ToggleStateManager


class QuestionFrame(EditableElement):
    def __init__(self, question_list: list[dict], parent_frame: Frame, function_manager: FunctionManager,
                 image_manager: ImageManager, state_manager: StateManager, toggle_state_manager: ToggleStateManager):
        super().__init__(parent_frame, bg="lightgray")
        self.__question_element_list = []
        self.__state_manager = state_manager
        self.__toggle_state_manager = toggle_state_manager
        self.add_functions(function_manager=function_manager)
        if question_list:
            self.set_questions(question_list=question_list, image_manager=image_manager,
                               function_manager=function_manager)
        else:
            self.__question_element_list.append(QuestionElement(image_manager=image_manager, parent_frame=self._frame,
                                                                remove_function=self.__remove_question,
                                                                function_manager=function_manager))

    def add_functions(self, function_manager: FunctionManager) -> None:
        function_manager.add_function("toggle_function", self.__toggle_function)

    def set_questions(self, question_list: list[dict], image_manager: ImageManager, function_manager: FunctionManager) -> None:
        self.unpack()
        self.__question_element_list.clear()
        for question_dict in question_list:
            question_element = QuestionElement(image_manager=image_manager,
                                                                parent_frame=self._frame,
                                                                initial_question=question_dict.get("question"),
                                                                initial_answer=question_dict.get("answer"),
                                                                remove_function=self.__remove_question,
                                                                function_manager=function_manager)
            self.__question_element_list.append(question_element)

    @property
    def get_all_question_dict(self) -> list[dict]:
        return [{"question": question_element.get_question, "answer": question_element.get_answer} for
                question_element in self.__question_element_list]

    def __remove_question(self, question: QuestionElement) -> bool:
        if len(self.__question_element_list) == 1:
            return False
        self.__question_element_list.remove(question)
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




