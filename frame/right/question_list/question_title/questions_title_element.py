from interface.editable_element import EditableElement
from settings import THEME_COLOR, MARGIN_BETWEEN_QUESTION
from utils.toggle_functions import toggle_button_image
from utils.element_functions import add_placeholder_to_frame
from helper_files import ImageManager
from tkinter import Frame, Entry, END, Button
from custom_elements import LogoButton
from helper_files import StateManager
from typing import Callable
from helper_files import FunctionManager


class QuestionTitleElement(EditableElement):
    def __init__(self, parent_frame: Frame, image_manager: ImageManager, state_manager: StateManager,
                 function_manager: FunctionManager, toggled_on: bool, title: str = ""):
        super().__init__(parent_frame, bg=THEME_COLOR, width=575, height=50)
        self.__parent_frame = parent_frame
        self.__image_manager = image_manager

        self.__title_entry = self.__get_title_entry()
        self.__add_function(function_manager=function_manager)
        self.__toggle_questions_button = self.__get_toggle_questions_button(toggled_on=toggled_on)
        self.__cancel_button = self.__get_cancel_button(function=lambda: function_manager.call_functions("revert_question"))
        self.__confirm_button = self.__get_confirm_button(function=lambda: function_manager.call_functions("save_question"))
        self.__remove_button = self.__get_remove_button(function=lambda: function_manager.call_functions("delete_question"))
        self.__edit_button = self.__get_edit_button(function=lambda: function_manager.call_functions("set_edit"))

        self.__setup(function_manager=function_manager)

        self.__state_manager = state_manager

        self.__set_title(title=title)

    def __add_function(self, function_manager: FunctionManager) -> None:
        function_manager.add_function("toggle_function", self.__toggle_button_image)

    def __setup(self, function_manager: FunctionManager) -> None:
        self.__toggle_questions_button.config(command=lambda: function_manager.call_functions("toggle_function"))

    def __toggle_button_image(self) -> None:
        toggle_button_image(button=self.__toggle_questions_button, first_image=self._frame.bring_down_image,
                            second_image=self._frame.bring_up_image)

    def __set_title(self, title: str) -> None:
        add_placeholder_to_frame(self.__title_entry, placeholder_text="Title")
        self.set_title(title=title)
        self.__title_entry.config(state="readonly")

    def __get_title_entry(self) -> Entry:
        return Entry(self._frame, width=25, font=("Calibri", 15))

    def __get_toggle_questions_button(self, toggled_on: bool) -> Button:
        bring_down_image = self.__image_manager.get_tkinter_image(name="down_logo.png", size=(22, 22))
        self._frame.bring_down_image = bring_down_image

        bring_up_image = self.__image_manager.get_tkinter_image(name="up_logo.png", size=(22, 22))
        self._frame.bring_up_image = bring_up_image

        image = bring_up_image if toggled_on else bring_down_image
        toggle_questions_button = LogoButton(self._frame, image=image,
                                             command=lambda: ..., background=THEME_COLOR)
        return toggle_questions_button

    def __get_cancel_button(self, function: Callable) -> Button:
        cancel_image = self.__image_manager.get_tkinter_image(name="x_logo.png", size=(20, 20))
        self._frame.cancel_image = cancel_image
        cancel_button = LogoButton(self._frame, image=cancel_image,
                                   command=function, background=THEME_COLOR)
        return cancel_button

    def __get_confirm_button(self, function: Callable) -> Button:
        confirm_image = self.__image_manager.get_tkinter_image(name="check_logo_thick.png", size=(24, 24))
        self._frame.confirm_image = confirm_image
        confirm_button = LogoButton(self._frame, image=confirm_image, command=function,
                                    background=THEME_COLOR)
        return confirm_button

    def __get_remove_button(self, function: Callable) -> Button:
        def button_function() -> None:
            self._frame.destroy()
            function()
        trash_image = self.__image_manager.get_tkinter_image(name="trash_can_logo.png", size=(30, 30))
        self._frame.trash_image = trash_image
        trash_button = LogoButton(self._frame, image=trash_image, command=button_function,
                                  background=THEME_COLOR)
        return trash_button

    def set_title(self, title: str) -> None:
        if title:
            self.__title_entry.delete(0, END)
            self.__title_entry.insert(0, title)
            self.__title_entry.config(fg="black")

    def __get_edit_button(self, function: Callable) -> Button:
        edit_image = self.__image_manager.get_tkinter_image(name="edit_logo.png", size=(45, 45))
        self._frame.edit_image = edit_image
        edit_button = LogoButton(self._frame, image=edit_image, command=function,
                                 background=THEME_COLOR)
        return edit_button

    def _base_pack(self) -> None:
        self._pack(padx=(0, MARGIN_BETWEEN_QUESTION))
        self.__title_entry.place(x=46, y=10)
        self.__toggle_questions_button.place(x=13, y=12)

    def pack_edit(self) -> None:
        self._base_pack()
        self.__cancel_button.place(x=507, y=13)
        self.__confirm_button.place(x=538, y=12)
        self.__remove_button.place(x=310, y=9)
        self.__title_entry.config(state="normal")

    def pack_view(self) -> None:
        self._base_pack()
        self.__edit_button.place(x=530, y=0)
        self.__title_entry.config(state="readonly")

    def pack(self) -> None:
        if self.__state_manager.on_editing_mode():
            self.pack_edit()
        else:
            self.pack_view()

    def unpack(self) -> None:
        self._unpack()
        self.__title_entry.place_forget()
        self.__toggle_questions_button.place_forget()
        self.__confirm_button.place_forget()
        self.__remove_button.place_forget()
        self.__cancel_button.place_forget()
        self.__edit_button.place_forget()

    @property
    def get_title(self) -> str:
        return self.__title_entry.get()