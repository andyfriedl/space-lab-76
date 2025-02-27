# Space Lab 76

**Space Lab 76** is a **retro-style isometric escape game** built with **Pygame**.  
You control **Bot**, a repair robot navigating through a failing space station.  
Your goal is to restore systems, scan objects in the correct order, unlock doors, and avoid patrolling enemy drones.

![Level 1](https://i.ibb.co/DH5J7jxf/Screenshot-2025-02-26-at-9-31-06-PM.png "Level 1")


---

## 🎮 How to Play

- **Move** ➜ Use **arrow keys** to navigate **Bot**.
- **Scan objects** ➜ Press **SPACE** near a wall object to scan it.
- **Collect items** ➜ Drive over floor items to pick them up (some restore power, others provide hints or hazards, and some dont do anything).
- **Unlock doors** ➜ Scan objects in the correct order to unlock doors. (Currently you only need to scan one item per room.)
- **Avoid enemies** ➜ Sentry Bots patrol the station and will drain your power and freeze you in place for a bit if they hit you.
- **Monitor power** ➜ Power depletes over time; collect power disks to stay operational.

---

## 🔥 Features

✅ **Built with Pygame** – Classic 2D rendering with an isometric perspective.  
✅ **Dynamic Level System** – Easily add or modify levels using JSON.  
✅ **Enemy AI** – Sentry Bots patrol and can damage the player.  
✅ **Power Management** – Power drains over time; collect certain items to restore it.  
✅ **Particle Effects** – Sparks appear when damaged, and energy waves trigger on successful scans.  
✅ **Modular Design** – Easily add new levels, objects, and mechanics.  

---

## 📁 Creating & Modifying Levels

Levels are stored in **`levels.json`**, allowing for easy modification or addition of new levels.

### **Key Level Properties**
- **`player_start`** → Defines Bot's starting position.
- **`objects`** → Interactive wall objects that can be scanned.
- **`progression`** → Defines the correct scan order and door unlocking mechanics.
- **`floor_items`** → Placed and random items that provide hints, restore power, or deal damage.
- **`sentries`** → Controls enemy count and speed.

### **Example Level Snippet**
```json
"level_1": {
    "player_start": { "x": 257, "y": 467 },
    "objects": [
        {"name": "printer_l", "interactive": true, "search_time": 1.0}
    ],
    "progression": {
        "interaction_order": ["printer_l", "door_floor_zone"],
        "unlock": ["door"]
    },
    "floor_items": {
        "random": { "count": 6, "directory": "floor_items/random" },
        "placed": [
            {
                "name": "5-14-floppy-red-tl",
                "x": 700,
                "y": 300,
                "effect": "hint",
                "hint_text": "Try scanning the printer\nPress SPACE."
            }
        ]
    }
}
```

## Adding New Objects & Items
- Wall objects → Any image in the assets/ folder can be referenced by name in levels.json.
- Random floor items → Place .png images in floor_items/random/, and they will automatically be included.
- Placed items → Define them manually in levels.json under "floor_items".
- Wear items → These do not interact with the player but serve as environmental details.

## Running the Game
### Install dependencies:
```
pip install pygame
```


### Run the game:
 ```
python main.py
```



## Visual Effects
- 🟥 Damage Effect → Sparks appear when Bot takes damage.
- 🟩 Success Effect → A glowing energy ring expands outward when Bot correctly scans an object.
- ⚡ Power Items → Some floor items restore Bot’s power when collected.

## 💡 Hints for New Players
- 🟢 Scanning is key! Scan the wall objects in the right order to unlock the door. Check floor items first, they can hold clues.
- 💾 Look for floor disks – Some provide power, others hints, but some may be hazards.
- 🔴 Avoid enemy drones – If they hit you, you'll lose power.
- 🚪 Doors don’t open automatically – Move into the door zone once you have scanned all required objects.
- 🔋 Your power drains over time – Keep an eye on the battery level.
- 📡 Scanning takes time – Be sure you’re scanning the right object before pressing SPACE.

