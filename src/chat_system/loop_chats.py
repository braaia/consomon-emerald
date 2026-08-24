import json, keyboard
from random import randint, choice, uniform
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

with open('json/backpack.json', 'r', encoding='utf-8') as arq:
    backpack = json.load(arq)

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

            sleep(0.4)
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

            action_choice = read_choice(["1", "2", "3"])

            match action_choice:
                case 1:
                    fight(backpack['team'][0], chosen_pokemon)
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
    global moves
    try:
        player_name = player['name']
        enemy_name = enemy['name']

        player_level = player['level']
        enemy_level = enemy['level']

        player_hp = player['current_stats']['hp']
        enemy_hp = enemy['current_stats']['hp']

        player_hp_max = player['current_stats']['hp']
        enemy_hp_max = enemy['current_stats']['hp']

        moveset = []
        for attack in player['moveset']:
            for move in moves:
                if attack['id'] == move['id']:
                    moveset.append(move)

        attack1 = moveset[0]['name'] if player_level >= player['moveset'][0]['level'] else "----------"
        attack2 = moveset[1]['name'] if player_level >= player['moveset'][1]['level'] else "----------"
        attack3 = moveset[2]['name'] if player_level >= player['moveset'][2]['level'] else "----------"
        attack4 = moveset[3]['name'] if player_level >= player['moveset'][3]['level'] else "----------"

        while True:
            try:
                if player_hp > 0:
                    if enemy_hp > 0:    
                        clear()
                        battle_text = (
                            f"{enemy_name:<10} Lv.{enemy_level:<2} {enemy_hp:>3.0f}/{enemy_hp_max:<3}"
                            f"{'VS':^16}\n"
                            f"{player_name:<10} Lv.{player_level:<2}{player_hp:>3.0f}/{player_hp_max:<3}\n"
                        )
                        print(Panel(battle_text, title="BATALHA POKÉMON", width=28))
                        print("\n[bold purple4]Escolha uma ação:")
                        print(f"""\n[red]1. Lutar
[green]2. Pokémon
[blue3]3. Bolsa
[bright_white]4. Fugir""")
                        
                        sleep(0.5)
                        action_choice = read_choice(["1", "2", "3", "4"])

                        if action_choice is None:
                            break

                        match action_choice:
                            case 1:
                                clear()
                                print(f"{player_name} Lv.{player_level}")
                                print("\n[bold purple4]Escolha um ataque:")

                                print(f"""1. {attack1}
2. {attack2}
3. {attack3}
4. {attack4}\n""")

                                attack_selection = read_choice(["1", "2", "3", "4"])

                                if attack_selection is None:
                                    continue

                                selected_attack = moveset[attack_selection - 1]

                                if player_level < player["moveset"][attack_selection - 1]["level"]:
                                    print("\n[bold red]Esse ataque ainda está bloqueado.[/bold red]")
                                    sleep(1)
                                    continue

                                player_hp, enemy_hp = fighting(
                                    player, enemy, selected_attack,
                                    player_name, enemy_name, player_hp, enemy_hp
                                )

                            case 2:
                                continue

                            case 3:
                                continue

                            case 4:
                                break
                    
                    else:
                        clear()
                        print(f"\n[bold]{enemy_name}[/bold] foi derrotado!")
                        print(skip)
                        keyboard.wait('space')
                        break                            
                else:
                    clear()
                    print(f"\nVocê foi derrotado!")
                    print(skip)
                    keyboard.wait('space')
                    break
            except Exception as error:
                print(f"[red]{error}")
    except:
        pass

def fighting(player, enemy, selected_attack, player_name, enemy_name, player_hp, enemy_hp):
    #region Status
    player_speed = player['current_stats']['speed']
    enemy_speed = enemy['current_stats']['speed']

    player_power = selected_attack['power']
    enemy_moveset = []
    for attack in enemy['moveset']:
        for move in moves:
            if attack['id'] == move['id']:
                enemy_moveset.append(move)
    enemy_move = choice(enemy_moveset)
    enemy_power = enemy_move['power']

    player_atk = player['current_stats']['atk']
    enemy_atk = enemy['current_stats']['atk']

    player_sp_atk = player['current_stats']['sp.atk']
    enemy_sp_atk = enemy['current_stats']['sp.atk']

    player_def = player['current_stats']['def']
    enemy_def = player['current_stats']['def']

    player_sp_def = player['current_stats']['sp.def']
    enemy_sp_def = enemy['current_stats']['sp.def']

    player_damage = (player_power * (player_atk/enemy_def) / 3) * uniform(0.9, 1.1)
    enemy_damage = (enemy_power * (enemy_atk/player_def) / 3) * uniform(0.9, 1.1)

    player_sp_damage = (player_power * (player_sp_atk/enemy_sp_def) / 3) * uniform(0.9, 1.1)
    enemy_sp_damage = (enemy_power * (enemy_sp_atk/player_sp_def) / 3) * uniform(0.9, 1.1)
    #endregion

    if selected_attack['category'] == "Physical":
        enemy_hp = max(0, enemy_hp - player_damage)
        with Progress() as prog:
            task = prog.add_task('Atacando...', total=10)
            while not prog.finished:
                sleep(0.2)
                prog.update(task, advance=2.7)
        print(f"""\n{player_name} usa {selected_attack['name']}!

É efetivo!

{enemy_name} perdeu {round(player_damage)} HP!""")
    elif selected_attack['category'] == "Special":
        enemy_hp = max(0, enemy_hp - player_sp_damage)
        with Progress() as prog:
            task = prog.add_task('Atacando...', total=10)
            while not prog.finished:
                sleep(0.2)
                prog.update(task, advance=2.7)
        print(f"""\n{player_name} usa {selected_attack['name']}!

É efetivo!

{enemy_name} perdeu {round(player_sp_damage)} HP!""")
        
    print(skip)
    keyboard.wait('space')
    return player_hp, enemy_hp


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
                    print(skip)
                    keyboard.wait("space")
                    continue

                case 2:
                    print(f"\nSeus Pokémons: {info['pokemon']}")
                    print(skip)
                    keyboard.wait("space")
                    continue
                
                case 3:
                    print(f"\nVocê possui: {info['pokeballs']}")
                    print(skip)
                    keyboard.wait("space")
                    continue
                
                case 4:
                    print(f"\nVocê possui: {info['items']}")
                    print(skip)
                    keyboard.wait("space")
                    continue
                
                case 5:
                    break
        except:
            pass


















    




