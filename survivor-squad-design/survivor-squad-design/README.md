# Survivor Squad: design pack

Coach from Left 4 Dead 2 as a playable Risk of Rain 2 Survivor, built from the real L4D2 files. Solo first.

## What is here

- `BRIEF.md`: the text to paste below the last line of a fresh Melty prompt. It carries the approved plan, so the agent skips the interview.
- `sheets/`: the design as JSON sheets. One row is one thing, one column is one property.
- `preflight.py`: run `python preflight.py` to list every unfilled cell, every unverified cell and every broken reference. `--md` prints Markdown.
- `PREFLIGHT.md`: the result as of this draft. The lists are long on purpose: nothing has been checked against the real games yet.

## How to use it

1. Unzip this folder into the project folder your agent works in (the PC that has Risk of Rain 2 and Left 4 Dead 2 installed).
2. In Melty, copy a fresh Publish prompt. It contains your token, so keep it out of files and commits.
3. Paste the text of `BRIEF.md` below the last line of that prompt, and send it to Claude Code or Codex on that PC.

## Sheet conventions

| Column kind | Meaning |
| --- | --- |
| `design` | Our own decision. Must be filled. Numbers are first guesses to tune in playtest. |
| `ref` | Points at a row in another sheet (`"to"` names the sheet; `"*"` means a `sheet.row` value). Must resolve. |
| `fact` | Something true about L4D2, RoR2 or Melty. Must be filled and checked. Its `check` says how: `l4d2-files`, `ror2-code` or `melty-tools`. |

- `"n/a"` counts as filled.
- A row's `verified` list names the fact columns that have been checked. Add a column there only after checking it.
- The sheets are the source of truth: change the sheet before the code.
- Build only when `python preflight.py` exits clean.

## Sheets

| File | What it holds |
| --- | --- |
| `01_games` | The two games and their roles (host and companion) |
| `02_survivors` | Coach (Ellis, Nick and Rochelle are later rows) |
| `03_skills` | The nine skill variants on the loadout screen |
| `04_weapons` | Assault rifle, pump shotgun, SMG, hunting rifle |
| `05_throwables` | Pipe bomb, Molotov, bile jar |
| `06_abilities` | Shove and Adrenaline |
| `07_animations` | Which L4D2 sequence plays for each RoR2 moment |
| `08_voice` | Coach's voice triggers |
| `09_assets` | Every L4D2 file the mod reads at runtime (none are uploaded) |
| `10_hooks` | Every RoR2 system the mod touches |

## Honest status

Draft 0, written without access to the games, to Melty or to RoR2's code. Every L4D2 path, sound-script entry, animation sequence name and RoR2 class name is a candidate until verified. The only L4D2 fact checked from outside sources is that the Survivors' internal names are Coach, Gambler, Mechanic and Producer.
