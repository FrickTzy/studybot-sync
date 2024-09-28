from tkinter import Frame, Toplevel, Entry, StringVar, OptionMenu, Button
from utils.window_functions import center_window
from utils.element_functions import add_placeholder_to_frame
from utils.generate_functions import generate_questions
from threading import Thread
from settings import THEME_COLOR
from typing import Callable


class GenerateQuestionsWindow:
    __WINDOW_NAME = "Question Generator"
    __WINDOW_SIZE = (400, 120)
    __PLACEHOLDER_TEXT = "Enter your topic here..."
    __DIFFICULTIES = ("Easy", "Medium", "Hard", "Random")

    def __init__(self, parent_frame: Frame, add_question_function: Callable):
        self.__window = Toplevel(parent_frame)
        self.__frame = Frame(self.__window, width=self.__WINDOW_SIZE[0], height=self.__WINDOW_SIZE[1], bg=THEME_COLOR)

        # Variables
        self.__topic_variable = StringVar(self.__frame)
        self.__question_variable = StringVar(self.__frame, value="10")
        self.__difficulty_variable = StringVar(self.__frame, value=self.__DIFFICULTIES[1])

        # Widgets
        self.__topic_entry = self.__create_topic_entry()
        self.__question_menu = self.__create_question_menu()
        self.__difficulty_menu = self.__create_difficulty_menu()
        self.__generate_button = self.__create_generate_button()

        # State control
        self.__currently_generating = False
        self.__add_question_function = add_question_function

        self.__setup()

    def pack(self) -> None:
        self.__frame.pack()
        self.__place_widgets()

    def __place_widgets(self) -> None:
        self.__topic_entry.place(x=20, y=10)
        self.__question_menu.place(x=135, y=55)
        self.__difficulty_menu.place(x=20, y=55)
        self.__generate_button.place(x=300, y=10)

    def __create_topic_entry(self) -> Entry:
        entry = Entry(self.__frame, font=("Calibri", 16, "bold"), width=24, textvariable=self.__topic_variable)
        add_placeholder_to_frame(entry=entry, placeholder_text=self.__PLACEHOLDER_TEXT)
        return entry

    def __create_question_menu(self) -> OptionMenu:
        options = [str(i) for i in range(5, 51, 5)]  # Questions from 5 to 50
        option_menu = OptionMenu(self.__frame, self.__question_variable, *options)
        option_menu.config(width=3, font=("Calibri", 12, "bold"), relief="raised", bd=2, highlightthickness=0)
        return option_menu

    def __create_difficulty_menu(self) -> OptionMenu:
        difficulty_menu = OptionMenu(self.__frame, self.__difficulty_variable, *self.__DIFFICULTIES)
        difficulty_menu.config(width=8, font=("Calibri", 12, "bold"), bd=2, highlightthickness=0)
        return difficulty_menu

    def __create_generate_button(self) -> Button:
        button = Button(self.__frame, text="Generate", font=("Calibri", 11, "bold"), command=self.__generate_questions)
        button.config(width=9)
        return button

    def __generate_questions(self) -> None:
        if self.__currently_generating:
            print(f"Please wait, currently generating.")
            return

        question_topic = self.__topic_variable.get()
        number_of_questions = self.__question_variable.get()
        difficulty = self.__difficulty_variable.get()

        if not question_topic or question_topic == self.__PLACEHOLDER_TEXT:
            print("Please input a topic.")
            return

        def start_generating():
            self.__currently_generating = True
            generated_questions = generate_questions(
                question_topic=question_topic,
                question_amount=int(number_of_questions),
                difficulty=difficulty
            )
            question_dict = {"title": question_topic, "questions": generated_questions}
            self.__add_question_function(question_dict)
            print("Finished Generating.")
            self.__currently_generating = False

        print(f"Generating {number_of_questions} questions for topic: {question_topic} at {difficulty} difficulty")
        Thread(target=start_generating, daemon=True).start()

    def __setup(self) -> None:
        self.__window.title(self.__WINDOW_NAME)
        center_window(window=self.__window, window_size=self.__WINDOW_SIZE)
