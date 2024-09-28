from tkinter import Frame, Label, Canvas, Scrollbar
from .question_list import QuestionMainFrame
from helper_files import ImageManager
from interface.frame_element import FrameElement
from .button_frame import ButtonFrame
from helper_files.state_manager import StateManager, ElementState
from typing import Optional, List


class RightSideFrame(FrameElement):
    """Frame to display and manage the list of questions on the right side of the UI."""

    def __init__(self, parent_frame: Frame, image_manager: ImageManager, questions_list: List[dict]) -> None:
        """Initialize the RightSideFrame with a list of questions and set up the canvas and scrollbar."""
        super().__init__(parent_frame=parent_frame, bg="white")

        # Setup main packing configuration
        self._set_packing_kwargs(packing_kwargs={"side": "right", "fill": "y"})

        # Initialize UI components
        self.__question_list = questions_list
        self.__image_manager = image_manager
        self.__pack_label()
        self.__create_scrollable_frame()
        self.__init_questions(questions_list=questions_list)

        # Add button frame at the bottom
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

    def add_question(self, question: dict) -> None:
        """Add a new question to the list and pack it into the scrollable frame."""
        state_manager = StateManager(state=ElementState.VIEW)
        QuestionMainFrame(
            parent_frame=self.scrollable_frame, question=question,
            image_manager=self.__image_manager, state_manager=state_manager
        ).pack()

    def create_question(self, question: Optional[dict] = None) -> None:
        """Create a new question and switch its state to edit mode."""
        if question is None:
            question = {}

        self.__question_list.append(question)
        state_manager = StateManager(state=ElementState.EDIT)
        QuestionMainFrame(
            parent_frame=self.scrollable_frame, question=question,
            image_manager=self.__image_manager, state_manager=state_manager
        ).pack()
