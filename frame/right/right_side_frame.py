from tkinter import Frame, Label, Canvas, Scrollbar
from .question_list import QuestionMainFrame
from helper_files import ImageManager
from helper_files.question_data_manager import delete_question, retrieve_questions_data, insert_question, add_question
from interface.frame_element import FrameElement
from .button_frame import ButtonFrame
from helper_files.state_manager import StateManager, ElementState
from typing import Optional, List
from utils.api import upload_question
from threading import Thread


class RightSideFrame(FrameElement):
    """Frame to display and manage the list of questions on the right side of the UI."""

    def __init__(self, parent_frame: Frame, image_manager: ImageManager) -> None:
        """Initialize the RightSideFrame with a list of questions and set up the canvas and scrollbar."""
        super().__init__(parent_frame=parent_frame, bg="white")

        self._set_packing_kwargs(packing_kwargs={"side": "right", "fill": "y"})

        self.__image_manager = image_manager
        self.__pack_label()
        self.__create_scrollable_frame()

        self.__question_frame_list: List[QuestionMainFrame] = []

        self.__init_questions(questions_list=retrieve_questions_data())

        ButtonFrame(parent_frame=self._frame, add_question_function=self.create_question).pack()

    def __pack_label(self) -> None:
        """Pack the label at the top of the right-side frame."""
        question_list_label = Label(self._frame, text="Question Lists", font=("Calibri", 16, "bold"), bg="white")
        question_list_label.pack(pady=(15, 5))

    def __create_scrollable_frame(self) -> None:
        """Create a scrollable canvas frame to hold the list of questions."""
        canvas_frame = Frame(self._frame)
        question_list_canvas = Canvas(canvas_frame, width=600, height=400, highlightthickness=0)
        scrollbar = Scrollbar(canvas_frame, orient="vertical", command=question_list_canvas.yview)

        self.scrollable_frame = Frame(question_list_canvas, width=590, height=400)
        self.scrollable_frame.bind(
            "<Configure>", lambda e: question_list_canvas.configure(scrollregion=question_list_canvas.bbox("all"))
        )

        # Configure the canvas with the scrollable frame and attach scrollbar
        question_list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        question_list_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar into the frame
        canvas_frame.pack(padx=10, pady=10)
        question_list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def __init_questions(self, questions_list: List[dict]) -> None:
        """Initialize the question frames from the provided list of questions."""
        for question in questions_list:
            self.add_question(question=question)

    def _pack_implementation(self) -> None:
        """Custom packing implementation. No additional packing needed for now."""
        pass

    def __upload_function(self, question_frame: QuestionMainFrame, question_dict: dict) -> None:
        for current_question_dict in retrieve_questions_data():
            current_question_dict["questionUploaded"] = False
        question_dict["questionUploaded"] = True

        delete_question(question_dict)
        insert_question(0, question_dict)

        self.__question_frame_list.remove(question_frame)
        self.__question_frame_list.insert(0, question_frame)

        Thread(target=lambda: upload_question(question_dict=question_dict)).start()

        self.__update_questions()

    def __delete_function(self, question_frame: QuestionMainFrame) -> None:
        self.__question_frame_list.remove(question_frame)

    def __pack_questions(self) -> None:
        for question_frame in self.__question_frame_list:
            question_frame.pack()

    def __unpack_questions(self) -> None:
        for question_frame in self.__question_frame_list:
            question_frame.unpack()

    def __update_questions(self) -> None:
        self.__unpack_questions()
        self.__pack_questions()

    def add_question(self, question: dict) -> None:
        """Add a new question to the list and pack it into the scrollable frame."""
        state_manager = StateManager(state=ElementState.VIEW)
        question_main_frame = QuestionMainFrame(
            parent_frame=self.scrollable_frame, question=question,
            image_manager=self.__image_manager, state_manager=state_manager,
            parent_upload_function=self.__upload_function,
            parent_delete_function=self.__delete_function,
        )
        question_main_frame.pack()
        self.__question_frame_list.append(question_main_frame)

    def create_question(self, question: Optional[dict] = None) -> None:
        """Create a new question and switch its state to edit mode."""
        if question is None:
            question = {}
        question["questionUploaded"] = False
        add_question(question)
        state_manager = StateManager(state=ElementState.EDIT)
        question_main_frame = QuestionMainFrame(
            parent_frame=self.scrollable_frame, question=question,
            image_manager=self.__image_manager, state_manager=state_manager,
            parent_upload_function=self.__upload_function,
            parent_delete_function=self.__delete_function,
        )
        question_main_frame.pack()
        self.__question_frame_list.append(question_main_frame)
