import pygame
import sys
import json
import menu
from config_validator import validate_config


def main() -> None:
    try:
        with open(sys.argv[1], "r") as f:
            lines = f.read()
            splitted_lines = lines.split("\n")
            json_lines = []
            for line in splitted_lines:
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                json_lines.append(stripped)
            json_lines = "\n".join(json_lines)
            config = json.loads(json_lines)
            if not isinstance(config, dict):
                print("Error: config file must contain a valid JSON Dict..")
                sys.exit(1)
            config = validate_config(config)
            pygame.init()
    except json.JSONDecodeError as e:
        print("Invalid JSON syntax:", e)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(1)
    except IndexError:
        print("Usage: python3 pacman.py <config.json>...")
        sys.exit(1)
    try:
        screen = pygame.display.set_mode((menu.WIDTH, menu.HEIGHT))
        pygame.display.set_caption("Pacman")
        background = pygame.image.load("graphics/BG.png").convert()
    except (pygame.error, FileNotFoundError) as e:
        print(f"Error: cannot load game assets: {e}")
        pygame.quit()
        sys.exit(1)
    while True:
        action = menu.run_menu(screen, background)
        if action == 0:
            pass
        elif action == 1:
            pass
        elif action == 2:
            run_instructions(screen, background)
        else:
            break
    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram Interrupted. Exiting..")
