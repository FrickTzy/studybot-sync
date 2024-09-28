from .element_state import ElementState


class StateManager:
    def __init__(self, state: ElementState):
        self.state = state

    def on_editing_mode(self) -> bool:
        return self.state == ElementState.EDIT