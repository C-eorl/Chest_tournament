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


class Repository:
    def add_db(self, data):
        self.db.insert(dict(data))


class TournamentRepository(Repository):
    def __init__(self, db):
        self.db = db

    def tournament_exist(self, name: str) -> bool:
        """ Renvoie True si nom est présent dans la base de donnée """
        TournamentQuery = Query()
        return bool(self.db.search(TournamentQuery.name == name))


class PlayerRepository(Repository):
    def __init__(self, db):
        self.db = db

    def player_search(self, id_chess):
        """ Recherche un joueur grâce à son id_chess"""
        JoueurQuery = Query()
        return self.db.get(JoueurQuery.id_chess == id_chess)

    def player_exist(self, id_chess: str) -> bool:
        """ Renvoie True si id_echec est présent dans la base de donnée """
        JoueurQuery = Query()
        return bool(self.db.search(JoueurQuery.id_chess == id_chess))

    def update_player(self, id_chess: str, valeur: dict):
        JoueurQuery = Query()
        self.db.update(valeur, JoueurQuery.id_chess == id_chess)

    def get_list_players(self):
        return self.db.all()
if __name__ == "__main__":

    initialization_db()
