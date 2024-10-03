

questions_data: list[dict] = []


def retrieve_questions_data() -> list[dict]:
    return questions_data


def set_questions_data(data: list) -> None:
    global questions_data
    questions_data = data


def delete_question(question: dict) -> None:
    questions_data.remove(question)


def insert_question(index: int, question: dict) -> None:
    questions_data.insert(index, question)


def add_question(question: dict) -> None:
    questions_data.append(question)
