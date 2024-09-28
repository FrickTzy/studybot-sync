from typing import Callable, Dict, List


class FunctionManager:
    """Uses observer pattern"""
    
    def __init__(self) -> None:
        self._function_dict: Dict[str, List[Callable]] = {}

    def add_function(self, type_name: str, function: Callable) -> None:
        """Adds a function to the observer under the specified type name."""
        if type_name not in self._function_dict:
            self._function_dict[type_name] = []
        self._function_dict[type_name].append(function)

    def call_functions(self, type_name: str) -> None:
        """Calls all functions associated with the specified type name."""
        if type_name not in self._function_dict:
            return
        for function in self._function_dict[type_name]:
            function()

