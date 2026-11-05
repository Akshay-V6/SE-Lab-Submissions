# Space Invaders Game

A Pygame Space Invaders clone updated for Lab 4 Vibe Coding.

## Changes made

- Fixed bullet/enemy collision handling so removing a hit bullet cannot skip the next bullet's collision check in that update.
- Added an in-window game-over and victory screen with final score.
- Added replay choices for Easy, Medium, and Hard, plus replay and exit controls.
- Added sound feedback for firing, enemy hits, and game over. The game still runs if audio is unavailable.

## Run

```bash
python -m pip install -r requirements.txt
python main.py
```

Move with **Left/Right** or **A/D** and fire with **Space**. On the end screen, press **1** for Easy, **2** for Medium, **3** for Hard, **R** to replay the same difficulty, or **Esc** to exit.

## Submission evidence

- `evidence/before.mp4` — baseline gameplay with the one-update collision skip reproduced and paused for inspection.
- `evidence/after.mp4` — gameplay after the collision fix, with sound, final-score screen, and a Hard-difficulty replay.
- `evidence/chat_history.pdf` — the actual lab-related exchange in this Codex session and a clearly labeled summary of the assistance provided.
