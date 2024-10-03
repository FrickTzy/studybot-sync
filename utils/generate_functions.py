from requests import get, post, exceptions
from settings import QUESTION_API_URL, GENERATE_CHOICES_API_URL


def generate_questions(question_topic: str, question_amount: int, difficulty: str) -> list[dict]:
    """Fetch questions from the API based on topic, amount, and difficulty."""
    params = {
        "topic": question_topic,
        "numberOfQuestions": question_amount,
        "difficulty": difficulty
    }
    print(f"Generating {question_amount} questions for topic: {question_topic} at {difficulty} difficulty")

    response = get(QUESTION_API_URL, params=params)
    try:
        response.raise_for_status()
        print("Generated Questions.")
        return response.json()
    except exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except exceptions.JSONDecodeError:
        print("Error decoding JSON. Retrying...")
    except exceptions.RequestException as err:
        print(f"Error generating questions: {err}")
    return generate_questions(question_topic, question_amount, difficulty)


def generate_choices(question_dict_list: list[dict]) -> list[dict]:
    """Post question choices to the API and return the response."""
    response = post(GENERATE_CHOICES_API_URL, json=question_dict_list)
    try:
        response.raise_for_status()
        print("Generated choices.")
        return response.json()
    except exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except exceptions.JSONDecodeError:
        print("Error decoding JSON response.")
    except exceptions.RequestException as err:
        print(f"Error generating choices: {err}")
