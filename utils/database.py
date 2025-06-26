import json
import os
from datetime import date

from tinydb import TinyDB
from models.joueur import Joueur

PATH_JOUEURS ="../data/joueurs/joueurs.json"
PATH_TOURNOIS ="../data/tournaments/tournois.json"


def initialisation_db():
    """
    Vérifie si les fichiers JSON et les dossiers parents existent, sinon, les créent
    :return: None
    """
    for path in [PATH_JOUEURS, PATH_TOURNOIS]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        nom_fichier = os.path.basename(path)
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            print("")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
                nom_fichier = os.path.basename(path)
                print(f"Creation de la base de donnée {nom_fichier}")
        else:
            print(f"La base de donnée {nom_fichier} existe déjà")


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


def get_db_joueurs() -> TinyDB:
    return TinyDB(PATH_JOUEURS)


def get_db_tournoi() -> TinyDB:
    return TinyDB(PATH_TOURNOIS)


if __name__ == "__main__":
    for path in [PATH_JOUEURS, PATH_TOURNOIS]:
        initialisation_db()
        format_db(path)