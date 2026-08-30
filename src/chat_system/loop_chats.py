import json, keyboard, random
from random import randint, choice, uniform
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from backend.backpack import load_backpack, view_backpack
from backend.poke_status import *
from backend.functions import clear, current_area, read_choice
from backend.world import exploring, process_area_events, current_area_id
from time import sleep


with open('json/pokedex.json', 'r', encoding='utf-8') as arq:
    pokedex = json.load(arq)

with open('json/areas.json', 'r', encoding='utf-8') as arq:
    areas = json.load(arq)

backpack = load_backpack()

skip = "\n[bold italic green1]Pressione espaço para continuar..."

def walking(area=current_area_id):
    area_name = current_area(area)

    while True:
        try:
            clear()    
            print(f"[bold italic]Você entrou na [/bold italic][bold]{area_name}\n")

            print(f"""[green]1. Explorar
[green3]2. Ir para trás
[yellow]3. Procurar Pokémon
[orange4]4. Abrir Inventário
[bright_magenta]5. Usar Poção
[red]6. Sair\n""")

            sleep(0.4)
            action_choice = read_choice(["1", "2", "3", "4", "5", "6"])

            if action_choice is None:
                break

            match action_choice:
                case 1:
                    exploring()
                    process_area_events()
                    print(skip)
                    keyboard.wait('space')
                    continue

                case 2:
                    exploring(False)
                    process_area_events()
                    print(skip)
                    keyboard.wait('space')
                    continue
                    
                case 3:
                    searching(searching=True)
                    print(skip)
                    keyboard.wait('space')
                    continue

                case 4:
                    open_backpack()
                    continue

                case 5:
                    print("[red bold]Em construção...")
                    print(skip)
                    keyboard.wait('space')
                    continue

                case 6:
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
                case 2:
                    pass
                case 3:
                    pass    
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

def calculate_xp(enemy_level):
    xp_table = [
        (1, 3, 40, 70),
        (4, 6, 60, 100),
        (7, 9, 90, 140),
        (10, 12, 120, 180),
        (13, 15, 160, 230),
        (16, 18, 210, 290),
        (19, 21, 270, 360),
        (22, 24, 330, 440),
        (25, 27, 400, 530),
        (28, 30, 470, 620),
        (31, 33, 550, 720),
        (34, 35, 650, 850)
    ]

    for min_level, max_level, min_xp, max_xp in xp_table:

        if min_level <= enemy_level <= max_level:
            return random.randint(min_xp, max_xp)

    return 0

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

        moveset = []
        for attack in player['moveset']:
            for move in moves:
                if attack['id'] == move['id']:
                    moveset.append(move)

        attack1 = moveset[0]['name'] if player_level >= player['moveset'][0]['level'] else "----------"
        attack2 = moveset[1]['name'] if player_level >= player['moveset'][1]['level'] else "----------"
        attack3 = moveset[2]['name'] if player_level >= player['moveset'][2]['level'] else "----------"
        attack4 = moveset[3]['name'] if player_level >= player['moveset'][3]['level'] else "----------"

        xp_gain = calculate_xp(enemy_level)

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
                        print(f"[bright_white]{enemy_name} ficou [bold red1]sem HP e desmaiou!\n")
                        print(f"[bright_white]Você ganhou [bold green3]{xp_gain} XP!")

                        lvl_up_system(backpack['team'][0], xp_gain)

                        print(skip)
                        keyboard.wait('space')
                        break                            
                else:
                    clear()
                    print(f"[bright_white]{player_name} ficou [bold red1]sem HP e desmaiou!\n")
                    print(f"\n[bright_white]Você foi [bold red1]derrotado!")

                    print(skip)
                    keyboard.wait('space')
                    break
            except Exception as error:
                print(f"[red]{error}")
    except:
        pass

def get_turn_order(player, enemy, player_move, enemy_move):
    player_order = (
        player_move.get("priority", 0),
        player["current_stats"]["speed"]
    )
    enemy_order = (
        enemy_move.get("priority", 0),
        enemy["current_stats"]["speed"]
    )

    if player_order > enemy_order:
        return ("player", "enemy")

    if enemy_order > player_order:
        return ("enemy", "player")

    return choice([
        ("player", "enemy"),
        ("enemy", "player")
    ])

def calculate_damage(attacker, defender, move):
    if move["category"] == "Physical":
        attack = attacker["current_stats"]["atk"]
        defense = defender["current_stats"]["def"]
    else:
        attack = attacker["current_stats"]["sp.atk"]
        defense = defender["current_stats"]["sp.def"]

    return (
        move["power"]
        * ((attack / max(1, defense))
        / 4)
        * uniform(0.9, 1.1)
    )

def fighting(player, enemy, selected_attack, player_name, enemy_name, player_hp, enemy_hp):
    enemy_moveset = []

    for attack in enemy['moveset']:
        for move in moves:
            if attack['id'] == move['id']:
                enemy_moveset.append(move)

    enemy_move = choice(enemy_moveset)

    turn_order = get_turn_order(
        player,
        enemy,
        selected_attack,
        enemy_move
    )

    for attacker in turn_order:
        if attacker == "player":
            if player_hp <= 0 or enemy_hp <= 0:
                break

            damage = calculate_damage(player, enemy, selected_attack)
            enemy_hp = max(0, enemy_hp - damage)

            with Progress() as prog:
                task = prog.add_task('Atacando...', total=10)
                while not prog.finished:
                    sleep(0.3)
                    prog.update(task, advance=2.5)

            print(
                f"\n[bold blue1]{player_name}[/bold blue1] [bright_white]usa[/bright_white] [bold italic bright_white]{selected_attack['name']}![/bold italic bright_white]\n"
                f"[bold italic red1]{enemy_name}[/bold italic red1] [italic bright_white]perdeu[/italic bright_white] [bold red1]{round(damage)} HP![/bold red1]\n"
            )

            sleep(2)

        else:
            if player_hp <= 0 or enemy_hp <= 0:
                break

            damage = calculate_damage(enemy, player, enemy_move)
            player_hp = max(0, player_hp - damage)

            with Progress() as prog:
                task = prog.add_task('Inimigo atacando...', total=10)
                while not prog.finished:
                    sleep(0.3)
                    prog.update(task, advance=2.5)

            print(
                f"\n[bold italic red1]{enemy_name}[/bold italic red1] [italic bright_white]usa[/italic bright_white] [bold bright_white]{enemy_move['name']}![/bold bright_white]\n"
                f"[bold blue1]{player_name}[/bold blue1] [bright_white]perdeu[/bright_white] [bold italic red1]{round(damage)} HP![/bold italic red1]\n"
            )

            sleep(2)
       
    print(skip)
    keyboard.wait('space')
    return player_hp, enemy_hp


def open_backpack():
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


















    




