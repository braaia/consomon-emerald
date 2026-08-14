import json
from pathlib import Path

BACKPACK_FILE = 'json/backpack.json'

def load_backpack():
    if Path(BACKPACK_FILE).exists():
        with open(BACKPACK_FILE, 'r', encoding='utf-8') as arq:
            return json.load(arq)
    else:
        return create_empty_backpack()


def create_empty_backpack():
    return {
        "pokemon": [],
        "pokeballs": [
            {"name": "Pokeball", "id": 1, "quantity": 0},
            {"name": "Superball", "id": 2, "quantity": 0},
            {"name": "Ultraball", "id": 3, "quantity": 0},
            {"name": "Masterball", "id": 4, "quantity": 0},
        ],
        "items": [
            {"name": "Fire Stone", "id": 101, "quantity": 0},
            {"name": "Water Stone", "id": 102, "quantity": 0},
            {"name": "Leaf Stone", "id": 103, "quantity": 0},
        ]
    }


def save_backpack(backpack):
    with open(BACKPACK_FILE, 'w', encoding='utf-8') as arq:
        json.dump(backpack, arq, indent=4, ensure_ascii=False)


def add_pokemon(backpack, pokemon):
    backpack["pokemon"].append(pokemon)
    save_backpack(backpack)


def add_pokeball(backpack, ball_id, quantity=1):
    for ball in backpack["pokeballs"]:
        if ball["id"] == ball_id:
            ball["quantity"] += quantity
            break
    save_backpack(backpack)


def add_item(backpack, item_id, quantity=1):
    for item in backpack["items"]:
        if item["id"] == item_id:
            item["quantity"] += quantity
            break
    save_backpack(backpack)


def remove_pokemon(backpack, pokemon_index):
    if 0 <= pokemon_index < len(backpack["pokemon"]):
        backpack["pokemon"].pop(pokemon_index)
        save_backpack(backpack)
        return True
    return False


def use_pokeball(backpack, ball_id, quantity=1):
    for ball in backpack["pokeballs"]:
        if ball["id"] == ball_id and ball["quantity"] >= quantity:
            ball["quantity"] -= quantity
            save_backpack(backpack)
            return True
    return False


def use_item(backpack, item_id, quantity=1):
    for item in backpack["items"]:
        if item["id"] == item_id and item["quantity"] >= quantity:
            item["quantity"] -= quantity
            save_backpack(backpack)
            return True
    return False


def view_backpack(backpack):
    info = {
        "pokemon_count": len(backpack["pokemon"]),
        "pokemon": [
            {"name": p.get("name", "?"), "level": p.get("level", "?")} 
            for p in backpack["pokemon"]
        ],
        "pokeballs": {
            ball["name"]: ball["quantity"] 
            for ball in backpack["pokeballs"]
        },
        "items": {
            item["name"]: item["quantity"] 
            for item in backpack["items"] 
            if item["quantity"] > 0
        }
    }
    return info