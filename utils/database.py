import json
import os
from tinydb import TinyDB
from dotenv import load_dotenv


load_dotenv()

PATH_PLAYERS = os.getenv("PATH_PLAYERS")
PATH_TOURNAMENTS = os.getenv("PATH_TOURNAMENTS")


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


def get_db_player():
    os.makedirs(os.path.dirname(PATH_PLAYERS), exist_ok=True)
    return TinyDB(PATH_PLAYERS)


def get_db_tournament() -> TinyDB:
    """Crée une TinyDB au chemin PATH_TOURNAMENTS"""
    os.makedirs(os.path.dirname(PATH_TOURNAMENTS), exist_ok=True)
    return TinyDB(PATH_TOURNAMENTS)
