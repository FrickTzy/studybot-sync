

class ToggleStateManager:
    def __init__(self, toggled_on: bool = True):
        self.__toggled_on = toggled_on

    def toggle(self) -> None:
        self.__toggled_on = not self.__toggled_on

    @property
    def toggled_on(self) -> bool:
        return self.__toggled_on
