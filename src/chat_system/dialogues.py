import keyboard
from time import sleep
from rich import print
from rich.progress import Progress
from backend.functions import slow_text, clear

def dialogue1():
    with Progress() as prog:
        task = prog.add_task("Iniciando Consomon Emerald...", total=10)
        while not prog.finished:
            sleep(0.3)
            prog.update(task, advance=2.2)
    sleep(0.8)
    clear()

    sleep(0.5)
    slow_text("??? - Olá!", False)
    sleep(0.4)
    slow_text(" Desculpe fazer você esperar.\n")

    sleep(0.8)
    slow_text("- Pressione espaço para continuar...")
    keyboard.wait('space')

    clear()
    sleep(0.5)
    slow_text("??? - Bem vindo ao mundo do Consomon.\n")
    keyboard.wait('space')

    slow_text("Birch - Meu nome é BIRCH.")
    sleep(0.4)
    slow_text("Mas todo mundo me chama de Professor Pokémon.")
    keyboard.wait('space')

    clear()
    sleep(0.2)
    slow_text("Este mundo é amplamente habitado por criaturas conhecidas como Pokémon.\n")
    keyboard.wait('space')

    slow_text("Nós,", False)
    sleep(0.3)
    slow_text(" humanos,", False)
    sleep(0.3)
    slow_text(" vivemos ao lado dos Pokémon —", False)
    sleep(0.3)
    slow_text(" às vezes como companheiros amigáveis ​​e,", False)
    sleep(0.3)
    slow_text(" outras vezes,", False)
    sleep(0.3)
    slow_text(" como parceiros de trabalho.")

    sleep(0.7)
    slow_text("e,", False)
    sleep(0.3)
    slow_text(" às vezes,", False)
    sleep(0.3)
    slow_text(" nos unimos e lutamos contra outros como nós.\n")
    keyboard.wait('space')

    clear()
    sleep(0.2)
    slow_text("Mas,", False)
    sleep(0.3)
    slow_text(" apesar da nossa proximidade,", False)
    sleep(0.3)
    slow_text(" não sabemos tudo sobre Pokémon.")
    keyboard.wait('space')


def birch_poke_choise():
    clear()

    sleep(0.5)
    slow_text("Birch - Eii!", False)
    sleep(0.4)
    slow_text(" Você ai!!")

    sleep(0.8)
    slow_text("Por favor!", False)
    sleep(0.4)
    slow_text(" Me ajude!\n")

    sleep(0.8)
    slow_text("- Pressione espaço para continuar...")
    keyboard.wait('space')

    clear()
    slow_text("Na minha bolsa tem algumas pokebolas!\n")
    keyboard.wait('space')






















