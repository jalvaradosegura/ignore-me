import json
from pathlib import Path
from typing import Dict, List, TypedDict

import questionary

RESOURCES_PATH = Path("questions")


class Question(TypedDict):
    question: str
    choices: List[str]
    correct: str
    explanation: str


def get_topics() -> Dict[str, List[Question]]:
    topics = {}

    for resource in RESOURCES_PATH.iterdir():
        with resource.open("r", encoding="utf-8") as f:
            questions = json.load(f)

        topics[resource.stem] = questions

    return topics


def ask_questions_amount() -> int:
    chosen_test_type = questionary.select(
        "Choose the amount of questions",
        choices=["10", "All"],
    ).ask()
    return int(10) if chosen_test_type == "10" else len(all_questions)


def start_test(questions: List[Question]) -> int:
    correct = 0
    for question in questions:
        result = questionary.select(
            question["question"], choices=question["choices"]
        ).ask()

        if result == question["correct"]:
            correct += 1
            print("✅ Correct\n")
        else:
            print("❌ Wrong\n")

        print(f"Explanation:\n{question['explanation']}\n")

    return correct


def summary(correct: int, questions_amount: int) -> None:
    print(
        "Summary:\n"
        f"You got {correct}/{questions_amount} -> {correct*100/questions_amount}%"
    )


if __name__ == "__main__":
    topics = get_topics()
    chosen_topic = questionary.select("Choose a topic", choices=topics.keys()).ask()
    all_questions = topics[chosen_topic]
    print("all_questions", all_questions)

    questions_amount = ask_questions_amount()

    questions = all_questions[:questions_amount]

    correct = start_test(questions)
    summary(correct, questions_amount)
