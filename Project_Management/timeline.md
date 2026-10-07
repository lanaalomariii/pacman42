# Project Timeline

## Duration 

The project was developed over a period of approximately 4 weeks, starting on 7/9/2026 and progressing from the initial planning phase to the final playable version.


## Approach

We used to-do list to track tasks, split between the two of us from day one (see [`team_organization.md`](./team_organization.md)). Day-to-day coordination happened through Slack and whatsApp, with code shared and reviewed through GitHub.


## Phases

### Setup & Meeting (7/9/2026 - 9/9/2026)
- Divided the project tasks between us and agreed on the shared tasks that we would work on together.
- Planned the overall structure of the project.

### Core Engine (10/9/2026 - 17/9/2026)
- Maze adapter, Player, Ghosts, config validation, highscore system.

### Game & Menu (18/9/2026 - 25/9/2026)
-`LevelManager`,`Game` `PacgumManager` classes, Score system and Menu.

### UI & Integration (25/9/2026 - 1/10/2026)
- Game screen, In-Game HUD, game-over and victory screens.

### Cheat Mode & Deployment (2/10/2026 - 6/10/2026)
- Cheat mode logic (invincibility, freeze, extra lives, level skip).
- Deploy on Itch.io.

## Team Collaboration

We communicated daily throughout the project via Slack and WhatsApp, coordinating tasks, reviewing each other's code, and discussing design decisions as they came up. 
Working together was a positive experience overall and the frequent check-ins helped us catch integration issues early rather than at the end.

As expected early on, the Ghost AI and the game screen (UI rendering) took longer than any other individual tasks. The ghost logic needed several rounds of debugging around its edible and respawning states, and the game screen took extra time both to learn Pygame's rendering model and to fix a performance issues.
