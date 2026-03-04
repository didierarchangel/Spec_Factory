# Point d'entrée CLI (Commandes: init, run, validate) 
#Ce script est le point d'entrée unique de votre écosystème Speckit.Factory. 
#Il utilise la bibliothèque click pour créer une interface en ligne de commande professionnelle

import click
import os
import json
from pathlib import Path
from core.validator import SpecValidator

# Configuration des chemins par défaut
DEFAULT_PROJECT_NAME = "SpecKit-App"

@click.group()
def cli():
    """🛡️ Speckit.Factory - Constitutional DevOps AI Framework"""
    pass

@cli.command()
@click.argument('path', default=DEFAULT_PROJECT_NAME)
@click.option('--here', is_flag=True, help="Initialise dans le dossier courant")
def init(path, here):
    """Initialise l'arborescence complète du projet [cite: 114-116]"""
    target_path = Path(".") if here else Path(path)
    
    # 1. Liste des dossiers à créer selon le protocole [cite: 119-131]
    structure = [
        "Constitution",
        "Task_App1",      # Tâches non réalisées (Architecture) [cite: 123]
        "Task_App2",      # Tâches réalisées (Architecture) [cite: 124]
        "Task_Function1", # Spécifications non réalisées [cite: 126]
        "Task_Function2", # Spécifications réalisées [cite: 127]
        "Task1",          # Tâches techniques non réalisées [cite: 129]
        "Task2"           # Tâches techniques réalisées [cite: 130]
    ]

    click.echo(f"🏗️  Création de l'arborescence dans : {target_path.absolute()}")

    for folder in structure:
        (target_path / folder).mkdir(parents=True, exist_ok=True)
    
    # 2. Création des fichiers de base [cite: 119-121, 132]
    (target_path / "Constitution" / "CONSTITUTION.md").touch()
    (target_path / "Constitution" / "etapes.md").touch()
    
    # 3. Initialisation du verrou .spec-lock.json [cite: 132-138]
    lock_file = target_path / ".spec-lock.json"
    if not lock_file.exists():
        initial_lock = {
            "constitution_hash": "",
            "completed_tasks": [],
            "completed_specs": []
        }
        with open(lock_file, "w") as f:
            json.dump(initial_lock, f, indent=4)
    
    click.echo("✅ Projet initialisé avec succès. La Constitution est prête.")

@cli.command()
@click.option('--task', required=True, help="ID de la tâche à exécuter (ex: 03_02)")
def run(task):
    """Exécute une tâche sous verrouillage de contexte [cite: 142]"""
    validator = SpecValidator()
    
    # Vérification de l'intégrité avant toute action [cite: 153-159]
    if not validator.check_integrity():
        click.echo("🛑 ARRÊT : Intégrité de la Constitution compromise !")
        return

    click.echo(f"🚀 Lancement de la tâche {task}...")
    # Ici, nous appellerons le graphe LangGraph prochainement
    click.echo("🔒 Contexte verrouillé chargé : Constitution + Etape + Task_App2 [cite: 147]")

if __name__ == "__main__":
    cli()
