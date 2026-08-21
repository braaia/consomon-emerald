from rich import print

def recalculate_stats(pokemon):
    """Calcula e atualiza os stats atuais com base no level e base_stats"""
    base = pokemon["base_stats"]

    pokemon["current_stats"] = {
        "hp": int(((base["hp"] * 2 + 20) * pokemon["level"] / 100) + pokemon["level"] + 10),
        "atk": int(((base["atk"] * 2 + 20) * pokemon["level"] / 100) + 5),
        "def": int(((base["def"] * 2 + 20) * pokemon["level"] / 100) + 5),
        "speed": int(((base["speed"] * 2 + 20) * pokemon["level"] / 100) + 5),
        "sp.atk": int(((base["sp.atk"] * 2 + 20) * pokemon["level"] / 100) + 5),
        "sp.def": int(((base["sp.def"] * 2 + 20) * pokemon["level"] / 100) + 5),
    }


def gain_exp(pokemon, amount):
    """Adiciona experiência e retorna informações sobre levelups ocorridos"""
    pokemon["exp"] += amount
    levelups = []

    while pokemon["exp"] >= pokemon["exp_to_next"]:
        # Guardar stats antigos ANTES de subir de level
        old_stats = pokemon["current_stats"].copy() if "current_stats" in pokemon else None
        
        # Aplicar a mudança de level
        pokemon["exp"] -= pokemon["exp_to_next"]
        pokemon["level"] += 1
        pokemon["exp_to_next"] = int(100 + (pokemon["level"] - 1) * 35)

        # Recalcular stats com o novo level
        recalculate_stats(pokemon)
        new_stats = pokemon["current_stats"]

        # Calcular diferenças
        if old_stats:
            stat_gains = {
                "hp": new_stats["hp"] - old_stats["hp"],
                "atk": new_stats["atk"] - old_stats["atk"],
                "def": new_stats["def"] - old_stats["def"],
                "speed": new_stats["speed"] - old_stats["speed"],
                "sp.atk": new_stats["sp.atk"] - old_stats["sp.atk"],
                "sp.def": new_stats["sp.def"] - old_stats["sp.def"],
            }
        else:
            stat_gains = {
                "hp": new_stats["hp"],
                "atk": new_stats["atk"],
                "def": new_stats["def"],
                "speed": new_stats["speed"],
                "sp.atk": new_stats["sp.atk"],
                "sp.def": new_stats["sp.def"],
            }

        # Guardar informação do levelup
        levelups.append({
            "new_level": pokemon["level"],
            "stat_gains": stat_gains,
            "new_stats": new_stats.copy()
        })

        if pokemon["level"] >= 16:
            pass

    return levelups

def lvl_up_system(pokemon, exp):
    levelups = gain_exp(pokemon, exp)

    if levelups:
        for levelup in levelups:
            print(f"\n[bold green]⭐ LEVEL UP! Nível {levelup['new_level']}[/bold green]")
            print("[bold]Ganhos de stats:[/bold]")
            for stat, gain in levelup['stat_gains'].items():
                print(f"  {stat.upper()}: +{gain}")
            print(f"[bold]Stats atuais:[/bold] {levelup['new_stats']}")
            print(f"[bold]XP necessário para o proximo nível:[/bold] {pokemon['exp']}/{pokemon['exp_to_next']}")
    else:
        print("\n[yellow]Nenhum levelup ocorreu[/yellow]")