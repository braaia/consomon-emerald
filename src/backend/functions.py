from rich import print
from time import sleep
import keyboard, os, sys

clear = lambda: os.system('cls')

def slowtext(text, newline=True):
    for i in list(text):
        print(i, end='')
        sys.stdout.flush()
        sleep(0.03)
    if newline:
        print()


def read_choice(valid_choices):
    while True:
        event = keyboard.read_event()

        if event.event_type != keyboard.KEY_DOWN:
            continue

        if event.name == "esc":
            return None

        if event.name in valid_choices:
            return int(event.name)

        print(
            f"[red bold]Pressione apenas: {', '.join(valid_choices)}[/red bold]",
            end="\r"
        )


def PokeChoise(pokedex):
    slowtext("PROF. BIRCH está com problemas!")
    sleep(0.5)
    slowtext("Escolha um Pokémon e resgate ele!\n")
    sleep(0.5)

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
    return my_pokemon