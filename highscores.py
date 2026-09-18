import json
import os
from typing import Any

MAX_NAME_LEN = 10
MAX_HIGHSCORES = 10


def is_valid_name(name: str) -> bool:
    """Check whether a highscore name is valid
    A valid name is non-empty contains at most 10 characters and
    contains only alphanumeric characters and spaces
    Args:
        name: name to validate
    Returns:
        True if name is valid otherwise False"""
    if len(name) > MAX_NAME_LEN or not name:
        return False
    for char in name:
        if not (char.isalnum() or char == " "):
            return False
    return True


def is_valid_score(score: int) -> bool:
    """Check whether a score is a valid non-negative integer"""
    return (
            isinstance(score, int)
            and not isinstance(score, bool) and score >= 0
            )


def load_highscores(file: str) -> list[dict[str, str | int]]:
    """Load valid highscores from a JSON file
    Returns an empty list if file doesn't exist,
    can't be read, invalid JSON, or has invalid data"""
    if not os.path.exists(file):
        return []
    try:
        with open(file, "r") as f:
            data: Any = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    valid = []
    for item in data:
        if (isinstance(item, dict)
                and "name" in item and "score" in item
                and isinstance(item["name"], str)
                and is_valid_name(item["name"])
                and is_valid_score(item["score"])):
            valid.append(item)
    return valid


def add_score(scores: list[dict[str, str | int]], name: str, score: int
              ) -> list[dict[str, str | int]]:
    """Add a valid score to the highscores
    Args:
        scores: Current highscore list
        name: player name
        score: player score
    Returns:
        the updated top highscores
    """
    if not is_valid_name(name) or not is_valid_score(score):
        return scores
    scores.append({"name": name, "score": score})
    scores.sort(key=lambda value: value["score"], reverse=True)
    return scores[:MAX_HIGHSCORES]


def save_highscores(file: str, scores: list[dict[str, str | int]]) -> None:
    """Save highscores to a JSON file"""
    try:
        with open(file, "w") as f:
            json.dump(scores[:MAX_HIGHSCORES], f)
    except OSError:
        print("Couldn't save")
