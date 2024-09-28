from tkinter import Frame
from interface.frame_element import FrameElement
from frame.right.question_list.question_title.questions_title_element import QuestionTitleElement
from .question_frame import QuestionFrame
from helper_files import ImageManager
from helper_files.state_manager.element_state import ElementState
from helper_files.state_manager.state_manager import StateManager
from helper_files.question_data_manager import delete_question
from helper_files.function_manager import FunctionManager
from helper_files.toggle_state_manager import ToggleStateManager


class QuestionMainFrame(FrameElement):
    __PADDING_X = 10
    __PADDING_Y = 10

    def __init__(self, question: dict, parent_frame: Frame,
                 image_manager: ImageManager, state_manager: StateManager):
        super().__init__(parent_frame=parent_frame)
        self.__state_manager = state_manager
        self.__main_question_dict = question
        self.__image_manager = image_manager

        toggled_on = self.__state_manager.on_editing_mode()
        self.__toggle_state_manager = ToggleStateManager(toggled_on=toggled_on)

        self.__function_manager = FunctionManager()
        self.__add_functions()
        self._set_packing_kwargs(packing_kwargs={"padx": self.__PADDING_X, "pady": self.__PADDING_Y})
        self.__question_frame = QuestionFrame(parent_frame=self._frame, question_list=question.get("questions"),
                                              image_manager=image_manager, state_manager=self.__state_manager,
                                              function_manager=self.__function_manager,
                                              toggle_state_manager=self.__toggle_state_manager)
        self.__title_element = QuestionTitleElement(parent_frame=self._frame, title=question.get("title"),
                                                    image_manager=image_manager, state_manager=self.__state_manager,
                                                    function_manager=self.__function_manager,
                                                    toggled_on=toggled_on)

    def __add_functions(self):
        self.__function_manager.add_function("save_question", self.__save_function)
        self.__function_manager.add_function("set_view", self.__set_view)
        self.__function_manager.add_function("delete_question", self.__delete_question)
        self.__function_manager.add_function("set_edit", self.__set_edit)
        self.__function_manager.add_function("revert_question", self.__revert_function)
        self.__function_manager.add_function("toggle_function", self.__toggle_state_manager.toggle)

    def __revert_function(self) -> None:
        if not self.__main_question_dict:
            self.__delete_question()
        else:
            self.__question_frame.set_questions(question_list=self.__main_question_dict["questions"],
                                                image_manager=self.__image_manager,
                                                function_manager=self.__function_manager)
            self.__title_element.set_title(title=self.__main_question_dict["title"])
            self.__function_manager.call_functions("set_view")

    def __save_function(self) -> None:
        self.__main_question_dict["questions"] = self.__question_frame.get_all_question_dict
        self.__main_question_dict["title"] = self.__title_element.get_title
        self.__function_manager.call_functions("set_view")

    def __delete_question(self) -> None:
        self._frame.destroy()
        delete_question(question=self.__main_question_dict)

    def _pack_implementation(self) -> None:
        self.__title_element.pack()
        self.__question_frame.pack()

    def pack(self) -> None:
        self._frame.pack(**self._packing_kwargs)
        self._pack_implementation()

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

