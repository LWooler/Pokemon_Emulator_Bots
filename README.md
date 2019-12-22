# Pokemon_Emulator_Bots
My collection of bots for finding shiny Pokémon on emulators

### Working:
All Pokémon Games
- Universal Soft Reset Bot (works for most emulators)
  - Features:
    - Programmable SR sequence
    - Stops and waits at encounter when detecting Shiny
    - Records SR count, and time elapsed
    - Will take picture of the encounter
  - Bug:
    - Has to be active window (cant use computer when running this bot) (possible workaround use a VM)
      - Unable to fix this as its a limitation of the ctype library used to send inputs

Pokémon Ruby/Sapphire (gba)
- Shiny Torchic Starter (mGBA emulator only)
  - Features:
    - Stops and waits at encounter when detecting Shiny Torchic
    - Records SR count, and time elapsed
    - Can run in the background (set and forget)
    - Will take picture of the encounter
    - (bug/feature) will also stop for uncatchable shiny poochyena/zigzagoon

### Planned:
Universal Soft Reset Bot
  - Planned Features:
    - Save/Load sequence

### Stretch Goals:
Universal Soft Reset Bot
  - Features:
    - GUI
    - Multiple Threading

Wild Encounter Shiny Bot
Egg Hatching Shiny Bot

### Development
- Python 3.7
