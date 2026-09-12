import random

CASES = {
    "free": {
        "name": "Бесплатно",
        "emoji": "🎁",
        "price": 0,
        "color": "#5865F2",
        "items": [
            {"name": "Common Bear", "emoji": "🐻", "value": 50, "rarity": "common", "weight": 500},
            {"name": "Rare Star", "emoji": "⭐", "value": 150, "rarity": "rare", "weight": 300},
            {"name": "Epic Gift", "emoji": "🎀", "value": 500, "rarity": "epic", "weight": 150},
            {"name": "Legendary Lamp", "emoji": "🪔", "value": 2000, "rarity": "legendary", "weight": 45},
            {"name": "Mythic Pen", "emoji": "🖊️", "value": 10000, "rarity": "mythic", "weight": 5},
        ]
    },
    "figure": {
        "name": "Figure",
        "emoji": "🎭",
        "price": 199,
        "color": "#5865F2",
        "items": [
            {"name": "Common Doll", "emoji": "🧸", "value": 80, "rarity": "common", "weight": 550},
            {"name": "Rare Mask", "emoji": "🎭", "value": 250, "rarity": "rare", "weight": 280},
            {"name": "Epic Crown", "emoji": "👑", "value": 800, "rarity": "epic", "weight": 130},
            {"name": "Legendary Ring", "emoji": "💍", "value": 3000, "rarity": "legendary", "weight": 35},
            {"name": "Mythic Diamond", "emoji": "💎", "value": 15000, "rarity": "mythic", "weight": 5},
        ]
    },
    "bear": {
        "name": "Bear",
        "emoji": "🐻",
        "price": 149,
        "color": "#FAA61A",
        "items": [
            {"name": "Small Bear", "emoji": "🧸", "value": 60, "rarity": "common", "weight": 560},
            {"name": "Happy Bear", "emoji": "🐻", "value": 200, "rarity": "rare", "weight": 270},
            {"name": "Angel Bear", "emoji": "😇", "value": 600, "rarity": "epic", "weight": 130},
            {"name": "King Bear", "emoji": "🦁", "value": 2500, "rarity": "legendary", "weight": 35},
            {"name": "Panda Gold", "emoji": "🐼", "value": 12000, "rarity": "mythic", "weight": 5},
        ]
    },
    "player": {
        "name": "Player",
        "emoji": "🎮",
        "price": 199,
        "color": "#EB459E",
        "items": [
            {"name": "Joystick", "emoji": "🕹️", "value": 80, "rarity": "common", "weight": 550},
            {"name": "Console", "emoji": "🎮", "value": 280, "rarity": "rare", "weight": 280},
            {"name": "VR Headset", "emoji": "🥽", "value": 900, "rarity": "epic", "weight": 130},
            {"name": "Neon Player", "emoji": "✨", "value": 3500, "rarity": "legendary", "weight": 35},
            {"name": "Golden Disc", "emoji": "💿", "value": 18000, "rarity": "mythic", "weight": 5},
        ]
    },
    "mood": {
        "name": "Mood",
        "emoji": "🎒",
        "price": 249,
        "color": "#57F287",
        "items": [
            {"name": "Backpack", "emoji": "🎒", "value": 100, "rarity": "common", "weight": 550},
            {"name": "Wings", "emoji": "🦋", "value": 350, "rarity": "rare", "weight": 280},
            {"name": "Rocket Pack", "emoji": "🚀", "value": 1200, "rarity": "epic", "weight": 130},
            {"name": "Angel Wings", "emoji": "👼", "value": 4500, "rarity": "legendary", "weight": 35},
            {"name": "Cloud Nine", "emoji": "☁️", "value": 22000, "rarity": "mythic", "weight": 5},
        ]
    },
    "skull": {
        "name": "Skull",
        "emoji": "💀",
        "price": 249,
        "color": "#ED4245",
        "items": [
            {"name": "Skull Ring", "emoji": "💍", "value": 100, "rarity": "common", "weight": 550},
            {"name": "Money Skull", "emoji": "💀", "value": 380, "rarity": "rare", "weight": 280},
            {"name": "Potion Red", "emoji": "🧪", "value": 1300, "rarity": "epic", "weight": 130},
            {"name": "Crown Skull", "emoji": "👑", "value": 5000, "rarity": "legendary", "weight": 35},
            {"name": "Golden Dead", "emoji": "🏴‍☠️", "value": 25000, "rarity": "mythic", "weight": 5},
        ]
    },
    "lamp": {
        "name": "Lamp",
        "emoji": "🪔",
        "price": 299,
        "color": "#FEE75C",
        "items": [
            {"name": "Old Lamp", "emoji": "🪔", "value": 120, "rarity": "common", "weight": 550},
            {"name": "Genie Blue", "emoji": "🧞", "value": 450, "rarity": "rare", "weight": 280},
            {"name": "Magic Watch", "emoji": "⌚", "value": 1500, "rarity": "epic", "weight": 130},
            {"name": "Wish Jar", "emoji": "🫙", "value": 6000, "rarity": "legendary", "weight": 35},
            {"name": "Genie King", "emoji": "🧞‍♂️", "value": 30000, "rarity": "mythic", "weight": 5},
        ]
    },
    "perfume": {
        "name": "Perfume",
        "emoji": "💐",
        "price": 399,
        "color": "#9B59B6",
        "items": [
            {"name": "Small Vial", "emoji": "🧪", "value": 150, "rarity": "common", "weight": 550},
            {"name": "Rose Box", "emoji": "📦", "value": 600, "rarity": "rare", "weight": 280},
            {"name": "UFC Pack", "emoji": "🥊", "value": 2000, "rarity": "epic", "weight": 130},
            {"name": "Rainbow", "emoji": "🌈", "value": 8000, "rarity": "legendary", "weight": 35},
            {"name": "Ice Perfume", "emoji": "❄️", "value": 40000, "rarity": "mythic", "weight": 5},
        ]
    },
}

RARITY_COLORS = {
    "common": "#8b95a5",
    "rare": "#3b82f6",
    "epic": "#a371f7",
    "legendary": "#ffcc00",
    "mythic": "#ef4444",
}

RARITY_NAMES = {
    "common": "Обычный",
    "rare": "Редкий",
    "epic": "Эпический",
    "legendary": "Легендарный",
    "mythic": "Мифический",
}

def open_case(case_id):
    case = CASES.get(case_id)
    if not case:
        return None
    items = case["items"]
    weights = [it["weight"] for it in items]
    return random.choices(items, weights=weights, k=1)[0]

def get_case_roll(case_id, win_index=35, length=50):
    case = CASES.get(case_id)
    if not case:
        return {"items": [], "win_index": 0}
    items = case["items"]
    weights = [it["weight"] for it in items]
    roll = random.choices(items, weights=weights, k=length)
    return {"items": roll, "win_index": win_index}
