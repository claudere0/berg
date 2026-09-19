# GAME DESIGN DOCUMENT: Berg & Woolly

## 1. High Concept
**Genre:** 2D Action-Platformer / Base-Defense Survival.
**Setting:** Pleistocene Epoch (Ice Age).
**Core Premise:** A solitary Ice Golem named Berg protects an abandoned woolly mammoth calf (Woolly) from prehistoric predators for 12 days until the mega-herd returns.
**Unique Selling Point (USP):** The player has no HP bar. Instead of dying, taking damage results in a temporary stun. All abilities, defenses, and resource logistics are tied to an aggressive "Ice Mana" economy.

## 2. Win & Loss Conditions
* **Win Condition:** Survive the 12th night. At dawn on the 13th day, the adult mammoth herd appears in the background, and predators scatter.
* **Loss Condition:** An enemy grabs Woolly and successfully drags him off any edge of the map. (Instant Game Over).

## 3. Core Gameplay Loop & Progression
The game spans 12 Days. Each day is split into Morning and Night phases. One full day cycle always equals exactly 120 seconds.
* **Morning (Safe Phase):** Enemy spawning is disabled. Berg explores the map, gathers resources, feeds Woolly, and builds defenses.
* **Night (Defense Phase):** The screen darkens. Predators spawn from the map edges and attempt to reach Woolly.

**Difficulty Curve (Time Scaling):**
* **Phase 1 (Tutorial, Days 1-3):** Morning 60s / Night 60s.
* **Phase 2 (Winter Begins, Days 4-6):** Morning 52.5s / Night 67.5s.
* **Phase 3 (Deep Freeze, Days 7-9):** Morning 45s / Night 75s.
* **Phase 4 (Glacial Hell, Days 10-12):** Morning 30s / Night 90s. Scavenging time is severely limited; pure survival mode.

## 4. Economy & Resources (The "Ice" System)
**Ice (Mana):** The core resource. Displayed as a blue bar in the UI. It regenerates passively (very slowly) and actively when Berg kills enemies using melee attacks (Dash / Ground Pound).

Ice is spent on 3 fundamental actions:
1. **Resource Gathering (Teleportation):** Pressing `E` at a tree/bush spends Ice to instantly teleport a Log (to the campfire) or Food (to Woolly). Berg doesn't need to manually carry items back.
2. **Offense (Ice Shards):** Pressing `F` shoots an ice projectile.
3. **Defense (Ice Blocks):** Pressing `V` spawns a durable Ice Wall in front of Berg. Maximum of 2-3 blocks allowed on the map at once.

*Note:* Resources (Trees and Bushes) take **3 in-game days to respawn**. This forces Berg to venture further away from the safe cave every morning.

## 5. Characters & Mechanics

### 5.1. Berg (The Ice Golem)
A highly mobile defender with no HP.
* **Knockdown (No Death):** If an enemy hits Berg, he falls and is stunned for 3 seconds. During this time, the player is helpless and must watch enemies run towards Woolly.
* **Variable Jump (Space):** Jump height depends on how long the button is held.
* **Ground Pound (Down Arrow in mid-air):** A drop attack that knocks back/stuns enemies in an AOE and generates Ice upon kills.
* **Dash / Snowball (Shift):** A rapid forward dash. Rams enemies for damage (generating Ice on kills) and allows Berg to cross the screen in a split second to save Woolly.

### 5.2. Woolly (The Mammoth Calf)
Stationary at the center of the map (the cave/base).
* **Cold Meter:** Constantly depletes. Restored when Berg "feeds" teleported logs to the central campfire.
* **Hunger Meter:** Constantly depletes. Restored when Berg feeds teleported bushes/roots directly to Woolly.
* If either meter hits zero, Woolly weakens, making it faster/easier for enemies to drag him away.

## 6. Bestiary (Enemies)
1. **Wolf:** Fast melee unit. Bites Berg (causing stuns) and gnaws on Ice Blocks. If it reaches Woolly, it slowly drags him toward the map edge.
2. **Cave Hyena:** Stealth unit. Completely ignores Berg, jumps over obstacles, grabs Woolly, and drags him very quickly. Top priority target.
3. **Cave Bear:** Slow Tank. Destroys Ice Blocks in a single hit. Acts as a battering ram for wolf packs.

## 7. Level Design & UI
* **The Map:** A single continuous level spanning 3 to 5 screens in width (camera scrolls to follow Berg). The cave (base) is in the center, flanked by forests with platforms and verticality.
* **Tiled (.tmx):** The map is built in the Tiled editor to easily place collision layers, enemy spawn points, platforms, and vegetation.
* **UI Radar (Critical):** Because the map is large, if Berg is far away and an enemy approaches Woolly, a large flashing red arrow appears on the edge of the screen accompanied by a trumpet sound (Woolly crying).

## 8. Technical Specs & Art Direction
* **Engine:** Python + Pygame + PyTMX.
* **Native Resolution:** `120 x 90` pixels.
* **Display Scaling:** Integer scaled x8 to `960 x 720` window size.
* **Palette Constraints:** Strict 27-color palette. RGB channels can only be `0`, `127`, or `255`. No transparency blending (1-bit alpha only).
* **UI Approach (Hybrid Render):** The game world is rendered at the chunky 120x90 resolution. However, Text, UI indicators, and the Radar are rendered **on top of the scaled-up 960x720 window**. This keeps the gameplay looking retro while ensuring text and UI elements remain crisp and readable.
