What I want

I already did the interview and approved a plan in a separate chat. Do the read-up first (connect to Melty; game_info for Risk of Rain 2 and Left 4 Dead 2; search_mashups; mashup_info on the closest one players can launch) and tell me in a few lines if anything there changes this plan. If nothing does, go ahead and build.

THE MASHUP
Survivor Squad (working title): Coach from Left 4 Dead 2 as a new playable Risk of Rain 2 Survivor, built from the real L4D2 files. Solo only for the first release: no co-op, no multiplayer listing.

THE GAMES
- Risk of Rain 2 is the host (role "primary"). Melty installs BepInEx 5 for it, and the mod is a BepInEx plugin.
- Left 4 Dead 2 is a companion: read from the player's own install through the folder Melty passes in (I suggest an environment variable of the mod's own, such as SURVIVORSQUAD_L4D2_DIR, set from {game:left-4-dead-2}). Nothing from L4D2 goes in the upload. No look-alike stand-ins, and no recipe.together, because the games do not run side by side.

WHAT THE PLAYER DOES
Press Play in Melty. Risk of Rain 2 starts, and Coach is on the character-select screen with his real model. On the loadout screen the player picks a gun (assault rifle, pump shotgun, SMG or hunting rifle) and a throwable (pipe bomb, Molotov or bile jar). Shove is the secondary and Adrenaline is the utility. In the stage, Coach uses L4D2's real gun sounds and animations, and his real voice lines react to the run (spawn, kill streaks, low health, reloading, throws, boss spawns, teleporter events).

THE FIRST PLAYABLE MUST HAVE
Coach with his real animated model and voice; the whole gear picker (4 guns, 3 throwables, Shove, Adrenaline); and a real screenshot or clip of Coach in a stage using a gun and a throwable.
Later releases, not now: Ellis, Nick and Rochelle, then co-op.

DESIGN SHEETS
If ./survivor-squad-design/ is in the project folder, start from its sheets/*.json. They are a first draft: every "fact" cell is a candidate from memory and still unverified (file paths, sequence names, RoR2 class names). Run `python preflight.py` before every build, change the sheet before the code, and build only when it is clean.

SUGGESTED ORDER
1. Toolchain: set up universal-modder, a BepInEx 5 plugin project, and decompile RoR2's assemblies.
2. L4D2 reader: VPK index, textures and materials, the model, animations, audio. First milestone: Coach standing in the character-select display.
3. Coach spawns, moves and jumps in a stage.
4. Assault rifle with reload, plus Shove.
5. The other guns and Adrenaline.
6. Throwables.
7. Voice triggers.
8. Loadout polish, package, one_click_check, a real install test, a real screenshot, and a draft listing.

RULES
- If part of the L4D2 reading proves unreliable (for example an animation set), tell me exactly which part and cut it. Do not fake it.
- If anything would need a manual install by the player, tell me before building.
- Bundle helper libraries only when their licenses allow it, with credit.
- Ask before anything that costs money.
- Propose the title, tagline, description, credits, license and remix choice once there is a real build. "Survivor Squad" is only a working title.
- Do not publish until I have seen the summary and said so.
