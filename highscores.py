import json
import os
from typing import Any


def is_valid_name(name: str) -> bool:
    if len(name) > 10 or not name:
        return False
    for char in name:
        if not (char.isalnum() or char == " "):
            return False
    return True


def is_valid_score(score: int) -> bool:
    return (
            isinstance(score, int)
            and not isinstance(score, bool) and score >= 0
            )


def load_highscores(file: str) -> list[dict[str, str | int]]:
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            data: Any = json.load(f)
    except (json.JSONDecodeError, OSError, FileNotFoundError):
        return []
    if not isinstance(data, list):
        return []
    valid = []
    for item in data:
        if (isinstance(item, dict)
                and "name" in item and "score" in item
                and is_valid_name(item["name"])
                and is_valid_score(item["score"])):
            valid.append(item)
    return valid


def add_score(scores: list[dict[str, str | int]], name: str, score: int
              ) -> list[dict[str, str | int]]:
    if not is_valid_name(name) or not is_valid_score(score):
        return scores
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda value: value["score"], reverse=True)
    return scores[:10]


def save_highscores(file: str, scores: list[dict[str, str | int]]) -> None:
    try:
        with open(file, "w") as f:
            json.dump(scores, f)
    except OSError:
        print("couldnt save")
