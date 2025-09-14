# Water Tank — Terminal Card Strategy Game (Python)

A quick, turn-based game against a simple AI. Your goal: finish with a tank level between **75–80** without overflowing. You’ll play water cards (1/5/10) and a few power cards to out-maneuver the computer.

## What’s inside
- **water_tank.py** — self-contained game script (no external deps).
- **Simple AI** — opponent uses a small heuristic to pick safe moves.
- **Clear I/O** — readable prompts, input validation, and status updates each turn.

## How to run
**Requirements:** Python 3.9+

```bash
# Windows / macOS / Linux
python water_tank.py
How to play (rules)
Start at 0. On your turn, play a water card: +1, +5, or +10.

Try to land in the 75–80 window to win.

If you go over 80, the overflow “bounces back” (you’ll lose that extra as a penalty).

Power cards (one-time plays):

SOH — Steal Opponent’s Half (take half of their current water).

DOT — Drain Opponent’s Tank (reduce their level).

DMT — Double My Tank (double your current level; risky near the cap).

First to end a turn in 75–80 wins. If both finish same turn, closest to 77.5 wins.

Example turn (truncated)
yaml
Copy code
Your tank: 42   |   Computer: 37
Available: [1, 5, 10, SOH, DOT, DMT]
Choose a card: 10

You played +10 → Your tank is now 52
Computer plays +5 → Computer is now 42
