*This activity has been created as part of the 42 curriculum by lalomari, fadarwis.*

# Pac-Man

## Description
This project is a Pac-Man-inspired game built in Python using object-oriented programming and Pygame. The game features a custom maze generated using the `A-Maze-ing` package assigned to us, used as-is through an adapter (`Maze` class) that exposes the operations the rest of the game needs, such as checking walls and computing neighbors.
Four ghosts, each with its own behaviour and targeting strategy:

**Blinky:** Chases Pac-Man's current position.

**Pinky:** Targets the position four cells ahead of Pac-Man in the direction they are facing.

**Inky:** Uses a combination of chasing and random movement (mostly chases the player).

**Clyde:** Chases Pac-Man when far away and returns to his starting position when he gets too close.

The game includes multiple levels, scoring, lives, a time limit, highscores and a configuration system.
The goal is to collect all pacgums and super-pacgums across at least 10 levels without losing all lives or running out of time.

## Instructions

### Installation
```bash
make install
```
This creates a local virtual environment (`venv/`) and installs all dependencies inside it (Pygame and the assigned `mazegenerator` package).

### Activate the virtual environment
```bash
source venv/bin/activate
```
### Running the game
```bash
make run
```
This launches the game using the default `config.json` file.

To run with a custom configuration file:
```bash
python3 pac-man.py path_to_custom_config.json
```
### Other Makefile targets
- `make debug` runs the game under Python debugger (pdb).
- `make lint` runs flake8 and mypy checks.
- `make clean` removes caches and the virtual environment.

### Controls
- Move: Arrow keys or WASD.
- ESC or P: Pause the game (you can choose to resume game or return to the main menu).
- I: Toggle invincibility (cheat).
- F: Toggle ghost freeze (cheat).
- N: Skip to the next level (cheat).
- E: Gain an extra life (cheat).

## Configuration

The game is configured through a JSON file passed as a command-line argument. Lines starting with `#` are treated as comments and ignored. If a key is missing or invalid, the game falls back to a safe default value and logs a message instead of crashing.

| Key | Description | Default |
|---|---|---|
| `highscore_filename` | File used to store highscores | `highscores.json` |
| `lives` | Starting number of lives | `3` |
| `pacgum` | Base number of pacgums for the first level | `150` |
| `points_per_pacgum` | Points for eating a pacgum | `10` |
| `points_per_super_pacgum` | Points for eating a super-pacgum | `50` |
| `points_per_ghost` | Points for eating an edible ghost | `200` |
| `level_max_time` | Time limit per level, in seconds | `90` |
| `levels` | List of 10 level configs, each with `width`, `height`, `seed` | see `config.json` |

The number of pacgums increases slightly with each level (`pacgum_count + current_level * 5`), while the maze size also increases with each level gradually raising the difficulty.

## Maze Generation

Mazes are generated using an external `A-Maze-ing` package assigned to us, used as-is through an adapter (`Maze` class) that exposes the operations the rest of the game needs (checking walls, computing neighbors, etc). The generator is called with `perfect=False` to produce Pac-Man-compatible corridors.

The first level always uses a fixed seed, so every playthrough starts identically. Every subsequent level uses a randomly generated seed, and the maze dimensions (`width`, `height`) increase gradually with each level as configured in `levels`. If maze generation fails for any reason, the error is caught and handled without crashing the game.

## Implementation
The game components were separated into different classes and files.

The `Game` class coordinates the main gameplay components(`Player`, `Ghost`, `PacgumManager`,`LevelManager`, `Score`), Ghost behaviour is described in Description section above. The ghosts use a Manhattan distance to pick their next step. This is a deliberate simplification compared with a full pathfinding search (such as BFS).

The game also implements lives, a level time limit, scoring, highscores, pause functionality, cheat mode, and different game states such as victory and game over.

## General Software Architecture
```text
├── config.json
├── config_validator.py
├── data
│   ├── highscores.py
│   └── __init__.py
├── game
│   ├── ghost.py
│   ├── __init__.py
│   ├── levels.py
│   ├── maze.py
│   ├── pacgum_manager.py
│   ├── player.py
│   └── score.py
├── game_.py
├── game_screen.py
├── graphics
│   ├── BG.png
│   ├── blinky.png
│   ├── clyde.png
│   ├── font.ttf
│   ├── grey.png
│   ├── highscore.png
│   ├── inky.png
│   ├── lose.png
│   ├── pacman.png
│   ├── Pause.png
│   ├── pinky.png
│   ├── time_up.png
│   └── win.png
├── highscores.json
├── Makefile
├── mazegenerator-2.1.0-py3-none-any.whl
├── menu.py
├── pac-man.py
├── Project_Management
│   ├── team_organization.md
│   └── timeline.md
└── README.md
```

The project is divided into two main packages:

- **`game/`** — the main game engine:
  - `maze.py` — adapter around the A-Maze-ing generator.
  - `player.py` — handles player movement, lives and respawning.
  - `ghost.py` — implements ghost behaviours and states.
  - `pacgum_manager.py` — handles pacgum and super-pacgum placement and collection.
  - `score.py` — manages score tracking.
  - `levels.py` — manages level progression, timers and difficulty scaling.

- **`data/`** - (`highscores.py`) - loads, validates, updates, and saves highscore data.
- **`graphics/`** - contains the images, fonts, and other visual assets used by the game and menu.
- `game_.py` — the `Game` class coordinating the main game components including pause/resume and cheat mode.
- `config_validator.py` sits between the raw JSON file and the rest of the game, producing a fully validated configuration dictionary.
- `game_screen.py` — handles the game screen, rendering, input, and the main game loop.
- `pac-man.py` - serves as the CLI entry point, loads and validates the configuration, initializes Pygame, and controls the transition between the main menu and the game.
- `menu.py` - handles the main menu and instructions screen, including navigation and user input.

##  Cheat mode

| Key | Effect |
|---|---|
| `I` | Toggle player invincibility |
| `F` | Toggle ghost freeze ((ghosts stop moving)|
| `N` | Skip to the next level |
| `E` | Gain an extra life |

## Highscore

Highscores are stored as a JSON file on disk (`highscores.json` by default). The system keeps the top 10 scores, each with a player name (max 10 alphanumeric characters and spaces) and a non-negative integer score. The file is loaded at the start of the game and saved whenever a new score is added after a game ends (win or loss). If
the file is missing, corrupted, or contains invalid entries, it is treated as empty instead of crashing. We chose a plain JSON file for simplicity and portability: it requires no external database and is easy to inspect and debug.

## Project Management

See the [`Project_Management/`](./Project_Management) directory for our timeline and team organization.

## Resources

- [Pygame documentation](https://www.pygame.org/docs/)
- [GeeksforGeeks Pygame Tutorial](https://www.geeksforgeeks.org/python/pygame-tutorial/)

### AI used
AI helped us with the Pygame part of the game screen, particularly with solving the problem of large images, scaling them correctly, positioning them inside the maze and designing the layout of name-entry screen.

AI also helped us implement the reachability check using BFS to make sure that pacgums are placed only on cells reachable from the player's starting position.
