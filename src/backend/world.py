import json
from rich import print
from backend.functions import CurrentArea, read_choice

with open('json/areas.json', 'r', encoding='utf-8') as arq:
    areas = json.load(arq)

current_area = areas['game_state']['current_area']


def Exploring(area = current_area):
    area_name = CurrentArea(area)


def process_area_events(area_id, world = areas):
    current_count = world['game_state']['explorations'].get(str(area_id), 0)

    direction = world['game_state']['chosen_paths']['direction']

    area = next(item for item in world['areas'] if item['id'] == area_id)

    for event in area['events']:
        if current_count == event['trigger_at_exploration']:
            if direction == event['direction']:
                print(f"Evento disparado: {event['type']}")
                resolve_event(event, world)

def resolve_event(event):
    if event["type"] == "path_choice":
        ...
    elif event["type"] == "item":
        ...
    elif event["type"] == "gym":
        ...