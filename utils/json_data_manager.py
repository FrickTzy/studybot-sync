from json import load, dump


class JsonDataManager:
    def __init__(self, json_path: str):
        self.__json_path = json_path

    def fetch_data(self) -> list:
        with open(self.__json_path, "r") as file:
            return load(file)

    def override_data(self, data: list) -> None:
        with open(self.__json_path, "w") as file:
            return dump(data, file)