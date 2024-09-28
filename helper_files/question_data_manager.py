

questions_data: list[dict] = []


def retrieve_questions_data() -> list[dict]:
    return questions_data


def set_questions_data(data: list) -> None:
    global questions_data
    questions_data = data


def delete_question(question: dict) -> None:
    questions_data.remove(question)
