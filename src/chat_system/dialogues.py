import keyboard
from time import sleep
from rich import print
from rich.progress import Progress
from backend.functions import slowtext, clear

def Dialogue1():
    with Progress() as prog:
        task = prog.add_task("Iniciando Consomon Emerald...", total=10)
        while not prog.finished:
            sleep(0.3)
            prog.update(task, advance=2.2)
    sleep(0.8)
    clear()

    sleep(0.5)
    slowtext("??? - Olá!", False)
    sleep(0.4)
    slowtext(" Desculpe fazer você esperar.\n")

    sleep(0.8)
    slowtext("- Pressione espaço para continuar...")
    keyboard.wait('space')

    clear()
    sleep(0.5)
    slowtext("??? - Bem vindo ao mundo do Consomon.\n")
    keyboard.wait('space')

    slowtext("Birch - Meu nome é BIRCH.")
    sleep(0.4)
    slowtext("Mas todo mundo me chama de Professor Pokémon.")
    keyboard.wait('space')

    clear()
    sleep(0.2)
    slowtext("Este mundo é amplamente habitado por criaturas conhecidas como Pokémon.\n")
    keyboard.wait('space')

    slowtext("Nós,", False)
    sleep(0.3)
    slowtext(" humanos,", False)
    sleep(0.3)
    slowtext(" vivemos ao lado dos Pokémon —", False)
    sleep(0.3)
    slowtext(" às vezes como companheiros amigáveis ​​e,", False)
    sleep(0.3)
    slowtext(" outras vezes,", False)
    sleep(0.3)
    slowtext(" como parceiros de trabalho.")

    sleep(0.7)
    slowtext("e,", False)
    sleep(0.3)
    slowtext(" às vezes,", False)
    sleep(0.3)
    slowtext(" nos unimos e lutamos contra outros como nós.\n")
    keyboard.wait('space')

    clear()
    sleep(0.2)
    slowtext("Mas,", False)
    sleep(0.3)
    slowtext(" apesar da nossa proximidade,", False)
    sleep(0.3)
    slowtext(" não sabemos tudo sobre Pokémon.")
    keyboard.wait('space')


def BirchPokeChoise():
    clear()

    sleep(0.5)
    slowtext("Birch - Eii!", False)
    sleep(0.4)
    slowtext(" Você ai!!")

    sleep(0.8)
    slowtext("Por favor!", False)
    sleep(0.4)
    slowtext(" Me ajude!\n")

    sleep(0.8)
    slowtext("- Pressione espaço para continuar...")
    keyboard.wait('space')

    clear()
    slowtext("Na minha bolsa tem algumas pokebolas!\n")
    keyboard.wait('space')






















