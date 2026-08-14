import keyboard, json, os
from rich import print
from rich.panel import Panel
from rich.progress import Progress
from time import sleep
from backend.poke_status import *

clear = lambda: os.system('cls')
clear()

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
[yellow]2. Procurar Pokemon
[orange4]3. Abrir Inventário
[bright_magenta]4. Usar Poção
[red]5. Sair\n""")
    
def Searching(area):
    current_area = CurrentArea(area)   

    print(f"Você está procurando na grama... ({current_area}[/green3])")

    with Progress() as prog:
        task = prog.add_task('Procurando...', total=15)
        while not prog.finished:
            sleep(0.3)
            prog.update(task, advance=2.3)

Searching(1)












# print(Panel("pokemon", subtitle=pokemon["level"], height=10, width=20, padding=(1, 2)))