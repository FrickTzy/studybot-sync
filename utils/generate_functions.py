from requests import get
from settings import QUESTION_API_URL


def generate_questions(question_topic: str, question_amount: int, difficulty: str) -> list[dict]:
    params = {
        "topic": question_topic,
        "numberOfQuestions": question_amount,
        "difficulty": difficulty
    }

    response = get(QUESTION_API_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error generating questions: {response.status_code} - {response.text}")
        return []
