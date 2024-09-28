from abc import abstractmethod, ABC
from tkinter import Frame


class FrameElement(ABC):
    """This class follows Template Design Pattern"""

    def __init__(self, parent_frame: Frame, **kwargs):
        self._frame = Frame(parent_frame, **kwargs)
        self._packing_kwargs = {}

    def _set_packing_kwargs(self, packing_kwargs: dict) -> None:
        self._packing_kwargs = packing_kwargs

    @abstractmethod
    def _pack_implementation(self) -> None:
        pass

    def pack(self) -> None:
        self._frame.pack(**self._packing_kwargs)
        self._pack_implementation()
