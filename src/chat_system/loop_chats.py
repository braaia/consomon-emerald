import json, keyboard
from random import randint
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from backend.backpack import load_backpack, view_backpack
from backend.poke_status import *
from backend.functions import clear, current_area, read_choice, slow_text
from backend.world import exploring, process_area_events
from time import sleep

with open('json/pokedex.json', 'r', encoding='utf-8') as arq:
    pokedex = json.load(arq)

with open('json/areas.json', 'r', encoding='utf-8') as arq:
    areas = json.load(arq)

backpack = load_backpack()
current_area_id = areas['game_state']['current_area']

skip = "\n[bold italic green1]Pressione espaço para continuar..."

def walking(area=current_area_id):
    global skip, areas
    area_name = current_area(area)

    while True:
        try:
            clear()    
            print(f"[bold italic]Você entrou na [/bold italic][bold]{area_name}\n")

            print(f"""[green]1. Explorar
[yellow]2. Procurar Pokémon
[orange4]3. Abrir Inventário
[bright_magenta]4. Usar Poção
[red]5. Sair\n""")

            sleep(0.5)
            action_choice = read_choice(["1", "2", "3", "4", "5"])

            if action_choice is None:
                break

            direction = areas['game_state']['chosen_paths']['direction']
            current_count = areas['game_state']['explorations'].get(str(current_area_id), {}).get(direction, 0)

            match action_choice:
                case 1:
                    exploring()
                    process_area_events()
                    print(skip)
                    keyboard.wait('space')
                    continue
                case 2:
                    searching(searching=True)
                    print(skip)
                    keyboard.wait('space')
                    continue
                case 3:
                    open_backpack()
                    print(skip)
                    keyboard.wait('space')
                    continue
                case 4:
                    print("[red bold]Em construção...")
                    print(skip)
                    keyboard.wait('space')
                    continue
                case 5:
                    with Progress() as prog:
                        task = prog.add_task('Saindo...', total=15)
                        while not prog.finished:
                            sleep(0.3)
                            prog.update(task, advance=2.7)
                    break
        except:
            pass
    

def searching(area=current_area_id, searching=False):
    area_name = current_area(area)   

    if searching:
        print(f"[bold italic]Você está procurando na grama... [/bold italic]({area_name})\n")

        with Progress() as prog:
            task = prog.add_task('Procurando...', total=15)
            while not prog.finished:
                sleep(0.3)
                prog.update(task, advance=2.7)
        sleep(1)
    clear()
    try:
        chance_find = randint(0,100)
        if chance_find <= 70:
            print("Um [green3]Pokémon selvagem[/green3] [bold]APARECEU!\n")

            list_pokemon = []

            i = 0
            for pokemon in pokedex:
                if pokemon['spawn'] == area:
                    i += 1
                    list_pokemon.append(pokemon)

            pokemon_id = randint(0, i-1)
            chosen_pokemon = list_pokemon[pokemon_id]

            match area:
                case 1:
                    exp = randint(100, 1125)
                    gain_exp(chosen_pokemon, exp)
                    print(exp)

                case 2:
                    exp = randint(1435, 4585)
                    gain_exp(chosen_pokemon, exp)
                    print(exp)

                case 3:
                    exp = randint(4585, 12060)
                    gain_exp(chosen_pokemon, exp)
                    print(exp)

                case 4:
                    exp = randint(12060, 23035)
                    gain_exp(chosen_pokemon, exp)
                    print(exp)

            print(Panel(f"{chosen_pokemon['name']}", subtitle=f"Level {chosen_pokemon['level']}", height=5, width=16, padding=(1, 3)))
            print(f"""\n[red]1. Lutar
[blue3]2. Capturar
[bright_white]3. Fugir""")
        else:
            print(chance_find)
            if searching:
                print("[bold red]Infelizmente vc teve azar e não conseguiu encontrar um Pokémon.")
            else:
                print("[bold red]Um pokémon apareceu mas fugiu!")

        return chosen_pokemon
    except:
        pass

with open("json/moves.json", "r", encoding="utf-8") as arq:
    moves = json.load(arq)

def fight(player, enemy):
    try:
        player_name = player['name']
        enemy_name = enemy['name']

        player_level = player['level']
        enemy_level = enemy['level']

        player_hp = player['current_stats']['hp']
        enemy_hp = enemy['current_stats']['hp']

        player_hp_max = player['current_stats']['hp']
        enemy_hp_max = enemy['current_stats']['hp']

        battle_text = (
            f"{enemy_name:<10} Lv.{enemy_level:<2} {enemy_hp:>3}/{enemy_hp_max:<3}"
            f"{'VS':^16}\n"
            f"{player_name:<10} Lv.{player_level:<2}{player_hp:>3}/{player_hp_max:<3}\n"
        )

        moveset = []
        for attack in player['moveset']:
            for move in moves:
                if attack['id'] == move['id']:
                    moveset.append(move)

        attack1 = moveset[0]['name'] if player['level'] >= player['moveset'][0]['level'] else "----------"
        attack2 = moveset[1]['name'] if player['level'] >= player['moveset'][1]['level'] else "----------"
        attack3 = moveset[2]['name'] if player['level'] >= player['moveset'][2]['level'] else "----------"
        attack4 = moveset[3]['name'] if player['level'] >= player['moveset'][3]['level'] else "----------"

        while True:
            try:
                clear()
                print(Panel(battle_text, title="BATALHA POKÉMON", width=28))
                print("\n[bold purple4]Escolha uma ação:")
                print(f"""\n[red]1. Lutar
[green]2. Pokémon
[blue3]3. Bolsa
[bright_white]4. Fugir""")
                
                sleep(0.5)
                action_choice = read_choice({"1", "2", "3", "4"})

                if action_choice is None:
                    break

                match action_choice:
                    case 1:
                        clear()
                        print(f"{player['name']} Lv.{player['level']}")
                        print("\n[bold purple4]Escolha um ataque:")

                        print(f"""1. {attack1}
2. {attack2}
3. {attack3}
4. {attack4}""")

                        attack_selection = read_choice(["1", "2", "3", "4"])

                        if attack_selection is None:
                            continue

                        selected_attack = moveset[attack_selection - 1]

                        if player["level"] < player["moveset"][attack_selection - 1]["level"]:
                            print("[bold red]Esse ataque ainda está bloqueado.[/red]")
                            sleep(1)
                            continue

                        fighting(player, enemy, selected_attack)

                    case 2:
                        continue

                    case 3:
                        continue

                    case 4:
                        break
            except Exception as error:
                print(f"[red]{error}")
    except:
        pass

def fighting(player, enemy, selected_attack):
    ...


def open_backpack():
    global skip
    info = view_backpack(backpack)

    while True:
        try:
            clear()
            print("[bold italic]Você está na mochila\n")
            print("""1. Quantidade de Pokémons
2. Nome dos Pokémons possuído
3. Quantidade de pokebolas
4. Quantidade de items
5. Sair\n""")

            sleep(1)
            inventory = read_choice(["1", "2", "3", "4", "5"])
            
            if inventory is None:
                break

            match inventory:
                case 1:
                    print(f"\nVocê possui: {info['pokemon_count']} Pokémons")
                    keyboard.wait("space")
                    print(skip)
                    continue

                case 2:
                    print(f"\nSeus Pokémons: {info['pokemon']}")
                    keyboard.wait("space")
                    print(skip)
                    continue
                
                case 3:
                    print(f"\nVocê possui: {info['pokeballs']}")
                    keyboard.wait("space")
                    print(skip)
                    continue
                
                case 4:
                    print(f"\nVocê possui: {info['items']}")
                    keyboard.wait("space")
                    print(skip)
                    continue
                
                case 5:
                    break
        except:
            pass


















    




