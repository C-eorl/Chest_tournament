import json
import os

from tinydb import TinyDB, Query
from dotenv import load_dotenv


load_dotenv()

PATH_PLAYERS = os.getenv("PATH_PLAYERS")
PATH_TOURNAMENTS = os.getenv("PATH_TOURNAMENTS")

def initialization_db():
    """
    Vérifie si les fichiers JSON et les dossiers parents existent, sinon, les créent
    :return: None
    """
    for path in [PATH_PLAYERS, PATH_TOURNAMENTS]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        name_file = os.path.basename(path)
        if not os.path.exists(path) or os.stat(path).st_size == 0:
            print("")
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
                name_file = os.path.basename(path)
                print(f"Creation de la base de donnée {name_file}")
        else:
            print(f"La base de donnée {name_file} existe déjà")


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

def get_db_player() -> TinyDB:
    return TinyDB(PATH_PLAYERS)

def get_db_tournament() -> TinyDB:
    return TinyDB(PATH_TOURNAMENTS)



if __name__ == "__main__":

    initialization_db()
