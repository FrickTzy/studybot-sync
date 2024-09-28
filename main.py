from tkinter import Tk, Frame
from helper_files.question_data_manager import set_questions_data, retrieve_questions_data
from helper_files import ImageManager
from utils import JsonDataManager
from utils.window_functions import center_window
from frame import HeaderFrame, LeftSideFrame, RightSideFrame


class StudyBotApp(Tk):
    __JSON_PATH = "json/questions.json"
    __TITLE = "StudyBot"
    __WINDOW_SIZE = (1000, 600)

    def __init__(self):
        super().__init__()
        self.__setup()
        self.__main_frame = Frame(self)
        self.__image_manager = ImageManager()
        self.__json_manager = JsonDataManager(json_path=self.__JSON_PATH)
        self.__store_initial_data()
        self.__header_frame = HeaderFrame(self.__main_frame, title=self.__TITLE)
        self.__left_frame = LeftSideFrame(self.__main_frame, questions_logs=[])
        self.__right_side_frame = RightSideFrame(self.__main_frame, image_manager=self.__image_manager,
                                                 questions_list=retrieve_questions_data())
        self.__set_quit_functions()
        self.__pack()

    def __store_initial_data(self) -> None:
        set_questions_data(data=self.__json_manager.fetch_data())

    def __setup(self) -> None:
        self.title(self.__TITLE)
        center_window(self, self.__WINDOW_SIZE)

    def __pack(self):
        self.__header_frame.pack()
        self.__left_frame.pack()
        self.__right_side_frame.pack()
        self.__main_frame.pack()

    def __set_quit_functions(self) -> None:
        def quit_function() -> None:
            self.__json_manager.override_data(data=retrieve_questions_data())
            self.destroy()

        self.protocol("WM_DELETE_WINDOW", quit_function)


if __name__ == "__main__":
    app = StudyBotApp()
    app.mainloop()
