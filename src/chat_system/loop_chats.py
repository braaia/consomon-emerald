import json, keyboard
from random import randint
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from backend.backpack import load_backpack, view_backpack
from backend.poke_status import *
from backend.functions import clear
from time import sleep

with open('json/pokedex.json', 'r', encoding='utf-8') as arq:
    pokedex = json.load(arq)

backpack = load_backpack()

def CurrentArea(area):
    area_atual = None
    match area:
        case 1:
            area_atual = "[green3]Floresta Petalburg Woods."
        case 2:
            area_atual = "[orange3]Rota 111 (Desertico)"
        case 3:
            area_atual = "[red3]Mt. Chimney"
        case 4:
            area_atual = "[blue3]Rota 119"
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


def OpenBackpack():
    info = view_backpack(backpack)

    print("[bold italic]Você está na mochila\n")
    print("""1. Quantidade de Pokémons
2. Nome dos Pokémons possuído
3. Quantidade de pokebolas
4. Quantidade de items
5. Sair\n""")

    while True:
        try:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == "esc":
                    break

                inventory = int(event.name)

                match inventory:
                    case 1:
                        print(f"\nVocê possui: {info['pokemon_count']} Pokémons")
                    case 2:
                        print(f"\nSeus Pokémons: {info['pokemon']}")
                    case 3:
                        print(f"\nVocê possui: {info['pokeballs']}")
                    case 4:
                        print(f"\nVocê possui: {info['items']}")
                    case 5:
                        break
                    case _:
                        print("[red bold]Por favor pressione apenas os números 1, 2, 3, 4 ou 5.[/red bold]", end="\r")
        except:
            print("[red bold]Por favor pressione apenas os números 1, 2, 3, 4 ou 5.[/red bold]", end="\r")


def Searching(area):
    current_area = CurrentArea(area)   

    print(f"Você está procurando na grama... ({current_area}[/green3])\n")

    with Progress() as prog:
        task = prog.add_task('Procurando...', total=15)
        while not prog.finished:
            sleep(0.3)
            prog.update(task, advance=2.7)
    sleep(1)
    clear()

    chance_find = randint(0,100)
    if chance_find <= 70:
        print("Um [green3]Pokémon selvagem[/green3] [bold]APARECEU!\n")

        list_pokemon = []

        i = 0
        for pokemon in pokedex:
            if pokemon['spawn'] == area:
                i += 1
                list_pokemon.append(pokemon)

        chosen_pokemon = randint(0, i-1)

        print(Panel(f"{list_pokemon[chosen_pokemon]['name']}", subtitle=f"Level {list_pokemon[chosen_pokemon]['level']}", height=5, width=16, padding=(1, 3)))
        print(f"""\n[red]1. Lutar
[blue3]2. Capturar
[bright_white]3. Fugir""")
    else:
        print("[red]Infelizmente vc teve azar e não conseguiu encontrar um Pokémon")



    




