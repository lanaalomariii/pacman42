from typing import Dict, List, Any

DEFAULT_LEVEL_COUNT = 10
DEFAULT_WIDTH = 15
DEFAULT_HEIGHT = 15
DEFAULT_SEED = 42

DEFAULTS: Dict[str, Any] = {
    "highscore_filename": "highscores.json",
    "lives": 3,
    "pacgum": 42,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "level_max_time": 90,
    "levels": [
        {"width": DEFAULT_WIDTH + i * 2,
         "height": DEFAULT_HEIGHT + i * 2,
         "seed": DEFAULT_SEED + i * 100}
        for i in range(DEFAULT_LEVEL_COUNT)
        ]
    }


def validate_positive_int(config: dict, key: str, default: int) -> int:
    value = config.get(key, default)
    if (not isinstance(value, int) or value <= 0) or (isinstance(value, bool)):
        print(f"Invalid value for key {key}, setting default...")
        value = default
    return value


def validate_levels(prev_levels: Any) -> List[Dict[str, int]]:
    if not prev_levels:
        print("Your list of levels is empty, setting default...")
        prev_levels = DEFAULTS["levels"]
    if not isinstance(prev_levels, list):
        print("Invalid format of levels..")
        print("Setting default levels..")
        prev_levels = DEFAULTS["levels"]
    else:
        levels_len = len(prev_levels)
        if levels_len < DEFAULT_LEVEL_COUNT:
            print("Insufficient number of levels...")
            print(f"Appending {DEFAULT_LEVEL_COUNT - levels_len}"
                  f"number of levels")
            prev_levels = (
                    prev_levels
                    + DEFAULTS["levels"][levels_len: DEFAULT_LEVEL_COUNT]
                    )
        if levels_len > DEFAULT_LEVEL_COUNT:
            print("Too many levels! the levels list will be truncated"
                  " to the default number of levels, which is 10 :)")
            prev_levels = prev_levels[:DEFAULT_LEVEL_COUNT]
        for i, level in enumerate(prev_levels):
            if not isinstance(level, dict):
                print("Invalid format of level <dict>..")
                print("Setting default level dict..")
                prev_levels[i] = dict(DEFAULTS["levels"][i])

            else:
                prev_levels[i]["width"] = validate_positive_int(
                        level, "width", DEFAULTS["levels"][i]["width"])
                prev_levels[i]["height"] = validate_positive_int(
                        level, "height", DEFAULTS["levels"][i]["height"])
                prev_levels[i]["seed"] = validate_positive_int(
                        level, "seed", DEFAULTS["levels"][i]["seed"])
    return prev_levels


def validate_config(config: dict) -> dict:
    valid_keys = ["highscore_filename", "lives", "pacgum",
                  "points_per_pacgum", "points_per_super_pacgum",
                  "points_per_ghost", "level_max_time", "levels"]
    new_config = {}
    for key in config:
        if key.lower() not in valid_keys:
            print("Invalid key detected...")
            continue
        new_config[key.lower()] = config[key]
    filename = new_config.get(
            "highscore_filename", DEFAULTS["highscore_filename"])
    if not isinstance(filename, str) or filename == "":
        print("Error: highscore_filename is either empty or invalid ...")
        print("Note: highscore_filename will be set to highscores.json")
        filename = DEFAULTS["highscore_filename"]
    new_config["highscore_filename"] = filename
    for key in valid_keys[1:7]:
        default = DEFAULTS[key]
        if key not in new_config:
            print(f"A {key} key is missing...oops..")
            print(f"Don't worry! we'll set it to default value"
                  f" of {default} for you :)")
        new_config[key] = validate_positive_int(new_config, key, default)
    new_config["levels"] = validate_levels(
            new_config.get("levels", DEFAULTS["levels"]))
    return new_config
