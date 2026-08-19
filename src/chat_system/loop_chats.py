import json, keyboard
from random import randint
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from backend.backpack import load_backpack, view_backpack
from backend.poke_status import *
from backend.functions import clear, slowtext, read_choice
from time import sleep

with open('json/pokedex.json', 'r', encoding='utf-8') as arq:
    pokedex = json.load(arq)

backpack = load_backpack()

def CurrentArea(area):
    area_atual = None
    match area:
        case 1:
            area_atual = "[green3]Floresta Petalburg Woods.[/green3]"

        case 2:
            area_atual = "[orange3]Rota 111 (Desertico)[/orange3]"

        case 3:
            area_atual = "[red3]Mt. Chimney[/red3]"

        case 4:
            area_atual = "[blue3]Rota 119[/blue3]"

    return area_atual
    

def Walking(area):
    current_area = CurrentArea(area)

    print(f"[bold italic]Você entrou na [/bold italic][bold]{current_area}\n")

    print(f"""[green]1. Explorar
[yellow]2. Procurar Pokémon
[orange4]3. Abrir Inventário
[bright_magenta]4. Usar Poção
[red]5. Sair\n""")


def Exploring(area):
    current_area = CurrentArea(area)


def Searching(area):
    current_area = CurrentArea(area)   

    print(f"Você está procurando na grama... ({current_area})\n")

    with Progress() as prog:
        task = prog.add_task('Procurando...', total=15)
        while not prog.finished:
            sleep(0.3)
            prog.update(task, advance=2.7)
    sleep(1)
    clear()
    try:
        chance_find = randint(0,100)
        if chance_find <= 100:
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
            print("[red]Infelizmente vc teve azar e não conseguiu encontrar um Pokémon")

        return chosen_pokemon
    except Exception as error:
        print(f"[red]{error}")

with open("json/moves.json", "r", encoding="utf-8") as arq:
    moves = json.load(arq)

def Fight(player, enemy):
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
                print("\n[purple4]Escolha uma ação:")
                print(f"""\n[red]1. Lutar
[green]2. Pokémon
[blue3]3. Bolsa
[bright_white]4. Fugir""")
                
                sleep(1)
                action_choice = read_choice({"1", "2", "3", "4"})

                if action_choice is None:
                    break

                match action_choice:
                    case 1:
                        clear()
                        print(f"{player['name']} Lv.{player['level']}")
                        print("\n[purple4]Escolha um ataque:")

                        print(f"""1. {attack1}
2. {attack2}
3. {attack3}
4. {attack4}""")

                        attack_selection = read_choice({"1", "2", "3", "4"})

                        if attack_selection is None:
                            continue

                        selected_attack = moveset[attack_selection - 1]

                        if player["level"] < player["moveset"][attack_selection - 1]["level"]:
                            print("[red]Esse ataque ainda está bloqueado.[/red]")
                            sleep(1)
                            continue

                        Fighting(player, enemy, selected_attack)

                    case 2:
                        continue

                    case 3:
                        continue

                    case 4:
                        break
            except Exception as error:
                print(f"[red]{error}")
    except Exception as error:
        print(f"[red]Erro ao iniciar a batalha: {error}[/red]")

def Fighting(player, enemy, selected_attack):
    ...

def OpenBackpack():
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
            inventory = read_choice({"1", "2", "3", "4", "5"})
            
            if inventory is None:
                break

            match inventory:
                case 1:
                    print(f"\nVocê possui: {info['pokemon_count']} Pokémons")
                    continue

                case 2:
                    print(f"\nSeus Pokémons: {info['pokemon']}")
                    continue
                
                case 3:
                    print(f"\nVocê possui: {info['pokeballs']}")
                    continue
                
                case 4:
                    print(f"\nVocê possui: {info['items']}")
                    continue
                
                case 5:
                    break
        except Exception as error:
            print(f"[red]{error}")


















    




