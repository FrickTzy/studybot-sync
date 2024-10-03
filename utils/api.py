from requests import post
from settings import UPLOAD_QUESTION_URL


def upload_question(question_dict: dict) -> None:
    post(UPLOAD_QUESTION_URL, json=question_dict)
    print("Uploaded the question to the database.")