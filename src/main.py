import json, keyboard
from rich import print
from loop_chats import *
from chat_system.dialogues import *
from backend.poke_status import *
from backend.backpack import *

with open('json/pokedex.json', 'r', encoding='utf-8') as arq:
    pokedex = json.load(arq)
for pokemon in pokedex:
    recalculate_stats(pokemon)
backpack = load_backpack()

print("--------========--------")
print("""1. [green]Treecko (Grass)[/green]
2. [red]Torchic (Fire)[/red]
3. [cyan]Mudkip (Water)[/cyan]""")
print("--------========--------")

while True:
    try:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "esc":
                break

            poke_init = int(event.name)

            match poke_init:
                case 1:
                    my_pokemon = pokedex[0]
                    break
                case 2:
                    my_pokemon = pokedex[1]
                    break
                case 3:
                    my_pokemon = pokedex[2]
                    break
                case _:
                    print("[red bold]Por favor pressione apenas os números 1, 2 ou 3.[/red bold]", end="\r")
    except:
        print("[red bold]Por favor pressione apenas os números 1, 2 ou 3.[/red bold]", end="\r")

if my_pokemon:
    add_pokemon(backpack, my_pokemon)
    info = view_backpack(backpack)
    print(f"\n[green]✓ {my_pokemon['name']} adicionado à mochila![/green]")
    print(f"[cyan]Pokémons na mochila: {info['pokemon_count']}[/cyan]")