# GAME DESIGN DOCUMENT: Berg (Arena Survival)

## 1. High Concept
**Genre:** 2D Arena Action-Platformer (Arcade).
**Setting:** Pleistocene Epoch (Ice Age).
**Core Premise:** The player controls an Ice Golem named Berg. The game takes place in a single closed Arena where the player must survive 12 escalating waves of prehistoric predators.
**Unique Selling Point (USP):** A fast-paced risk/reward combat loop. Aggressive melee combat generates "Ice" (Mana), which can be spent on safer ranged attacks and creating defensive cover. 

## 2. Win & Loss Conditions
* **Wave Victory:** Destroy a specific number of enemies (e.g., "Enemies killed: 0/30"). This forces aggressive play rather than just running away until a timer runs out.
* **Global Victory:** Clear the 12th (Final) wave.
* **Loss Condition:** Lose all 3 Health Points (HP). Results in a restart of the current wave (or the entire run, depending on final difficulty tuning).

## 3. Character: Berg (The Ice Golem)
Berg has **3 HP (Ice Crystals above his head)**. Upon taking damage, he loses 1 HP, is knocked back, and gains 1 second of invulnerability.

**Moveset (Abilities):**
* **Variable Jump (Space):** Jump height depends on how long the key is held.
* **Dash / Snowball (Shift):** A rapid horizontal dash. Rams enemies, dealing damage and knocking them back.
* **Ground Pound (Down Arrow in mid-air):** Berg drops like a stone, dealing Area of Effect (AOE) damage to all enemies directly beneath him.

**Ice Economy (Mana):**
* Killing an enemy with a melee attack (Dash or Ground Pound) **restores** Ice Mana.
* **Ice Shard (F):** Costs a small amount of Mana. Shoots a projectile to kill agile enemies from a distance.
* **Ice Block (V):** Costs a large amount of Mana. Spawns an ice cube in front of Berg. Can be used as a barricade to block enemies or as a platform to reach higher ground.

## 4. Arena & Visual Progression
**The Map:** There is only **ONE** Arena. Size: 1.5 to 2 screens wide (the camera smoothly follows the player). The arena contains platforms of varying heights to encourage vertical gameplay.
**Atmosphere Progression:** To keep the game visually engaging without creating new maps, the color palette and weather change dynamically as waves progress:
* **Waves 1-3:** Bright day, white snow, clear skies.
* **Waves 4-6:** Sunset, orange/red sky, long dark shadows.
* **Waves 7-9:** Dusk, low light, light snowfall begins.
* **Waves 10-12:** Deep night, severe blizzard (reduced visibility, horizontal snow effects).

## 5. Bestiary (Enemies)
Enemies spawn from the edges of the screen or dark caves in the background.
1. **Wolf:** Basic runner. Runs straight at the player and can jump onto low platforms.
2. **Cave Hyena:** Agile jumper. Navigates the upper platforms quickly and tries to drop on Berg from above. Prime target for Ice Shards.
3. **Cave Bear:** The Tank. Moves slowly but takes up a lot of space. Destroys Berg's Ice Blocks in a single hit. Absorbs multiple hits before dying.

## 6. Wave Progression
* **Wave 1:** 10 Wolves. (Teaches basic movement and melee).
* **Wave 2:** 15 Wolves. (Teaches Dashing into crowds).
* **Wave 3:** 20 Wolves. High spawn density.
* **Wave 4:** 15 Wolves + 5 Hyenas. (Teaches shooting upward/ranged combat).
* **Wave 5:** 10 Hyenas. (A test of platforming agility).
* **Wave 6:** 20 Wolves + 10 Hyenas. 
* **Wave 7:** 1 Cave Bear + 10 Wolves. (Teaches kiting tank enemies).
* **Waves 8-11:** Escalating chaos. A frantic mix of all three enemy types.
* **Wave 12 (Finale):** A massive horde during a blinding blizzard. Survival relies on perfect reflexes and mana management.

## 7. Technical Specifications
* **Engine:** Python + Pygame.
* **Native Resolution:** 120 x 90 pixels (Retro Arcade feel).
* **Display Scaling:** Integer scaled x8 to 960 x 720.
* **Palette Constraints:** Strict 27-color palette (RGB channels limited to 0, 127, or 255).
* **UI Approach (Hybrid Render):** The game world is pixelated (120x90), but the UI (HP crystals, kill counter, wave number) is rendered at high resolution on the scaled-up window for crisp readability.
