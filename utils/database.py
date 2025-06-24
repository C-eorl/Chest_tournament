import json
import os
from datetime import date

from tinydb import TinyDB
from models.joueur import Joueur

PATH_JOUEURS ="../data/joueurs/joueurs.json"
PATH_TOURNOIS ="../data/tournaments/tournois.json"


def initialisation_db(path):
    """
    Vérifie l'existance du dossier et du fichier .json
    :param path:
    :return:
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if not os.path.exists(path) or os.stat(path).st_size == 0:
        with open(path, "w", encoding="utf-8") as f:
            json.dump({}, f)  # initialise avec un objet vide


def format_db(path: str):
    """
    formate la tinyDB pour une version plus lisible
    :param path: chemin relatif vers le fichier .json
    :return: None
    """
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():  # fichier vide
        return f"Fichier vide : {path}, on saute le formatage."

    data = json.loads(content)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    for path in [PATH_JOUEURS, PATH_TOURNOIS]:
        initialisation_db(path)
        format_db(path)