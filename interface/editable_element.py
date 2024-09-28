from abc import ABC, abstractmethod
from tkinter import Frame


class EditableElement(ABC):
    def __init__(self, parent_frame: Frame, **kwargs):
        self._frame = Frame(parent_frame, **kwargs)

    def _pack(self, *args, **kwargs):
        self._frame.pack(*args, **kwargs)

    def _unpack(self):
        self._frame.pack_forget()

    @abstractmethod
    def _base_pack(self) -> None:
        pass

    @abstractmethod
    def pack_view(self) -> None:
        pass

    @abstractmethod
    def pack_edit(self) -> None:
        pass
