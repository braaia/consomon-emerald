import json
from random import randint, choice
from rich import print
from backend.functions import current_area, read_choice, slow_text

with open('json/areas.json', 'r', encoding='utf-8') as arq:
    areas = json.load(arq)

current_area_id = areas['game_state']['current_area']
direction = areas['game_state']['chosen_paths']['direction']


def exploring(area_id=current_area_id):
    from chat_system.loop_chats import searching
    global areas

    explorations = areas["game_state"]["explorations"].get(str(current_area_id), {}).get(direction, 0)
    explorations += 1
    areas['game_state']['explorations'][str(area_id)][direction] = explorations

    steps = f"[bright_white bold italic]Explorações na área:[/bright_white bold italic] [bold blue1]{areas['game_state']['explorations'][str(area_id)][direction]}/10"
    print(areas['game_state']['explorations'][str(area_id)][direction])

    chance = randint(1, 100)

    if chance <= 20:
        searching()
        return
    
    if chance <= 50:
        messages = [
            "Você caminha entre as árvores e não encontra nada além de folhas secas.",
            "O caminho continua silencioso, mas o vento parece mudar de direção.",
            "Você segue avançando, mas a trilha parece vazia por agora.",
            "Você inspeciona o entorno, mas nada de interessante aparece."
        ]
        slow_text(choice(messages))
        print(steps)
        return

    if chance <= 70:
        messages = [
            "Você escuta um movimento entre as árvores.",
            "Há uma sombra se movendo em meio ao mato.",
            "Você percebe rastros recentes no chão.",
            "A vegetação se mexe e há sinais de um Pokémon por perto."
        ]
        slow_text(choice(messages))
        print(steps)
        return

    if chance <= 100:
        messages = [
            "Você descobre um caminho novo entre a vegetação.",
            "Um atalho parece abrir uma nova rota pela área.",
            "Você encontra uma pista que sugere um caminho diferente.",
            "Há uma passagem escondida que pode ser útil mais tarde."
        ]
        slow_text(choice(messages))
        print(steps)
        return

    # if chance <= 70:
    #     messages = [
    #         "Você encontra um item escondido entre a vegetação.",
    #         "Algo brilha entre as raízes e você pega uma Pokébola.",
    #         "Você revirando o chão encontra um item raro.",
    #         "No meio do mato, um objeto útil foi deixado para trás."
    #     ]
    #     print(choice(messages))
    #     print("+1 Pokébola")
    #     return


def process_area_events(area_id=current_area_id):
    global current_area_id, areas, direction
    area_name = current_area(area_id)

    current_count = areas['game_state']['explorations'].get(str(area_id), {}).get(direction, 0)
    defeated_gyms = areas['game_state']['defeated_gyms']

    area = next(item for item in areas['areas'] if item['id'] == area_id)

    for event in area['events']:
        if current_count == event['trigger_at_exploration']:
            if direction == event['direction']:
                print(f"Evento disparado: {event['type']}")
                resolve_event(event)

    unlock = area['unlocks']

    if current_count == unlock['required_explorations'] and direction == unlock['direction']:
        if unlock['required_gym'] in defeated_gyms:
            print(current_area_id)
            print(f"[bold italic] Deseja ir para {area_name}?")
            current_area_id = unlock['to_area']
            print(current_area_id)
        else:
            print("[red bold]Para prosseguir, você precisa derrotar o líder de ginásio dessa cidade primeiro!")

def resolve_event(event):
    if event["type"] == "path_choice":
        ...
    elif event["type"] == "item":
        ...
    elif event["type"] == "gym":
        ...