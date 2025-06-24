from datetime import date

from tinydb import TinyDB
from models.joueur import Joueur

def initialisation_db_joueur():
    path = "../data/joueurs/joueurs.json"
    return TinyDB(path)

def initialisation_db_tournoi():
    path = "../data/joueurs/tournois.json"
    return TinyDB(path)


if __name__ == "__main__":
  pass