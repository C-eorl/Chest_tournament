from datetime import datetime

from tinydb import Query

from match import Match
from utils import database


class Tour:
    def __init__(self, list_match: list[Match], nom: str, date_heure_fin):
        self.list_match = list_match
        self.nom = nom
        self.date_heure_debut = datetime.now()
        self.date_heure_fin = date_heure_fin

    def __str__(self):
        return f"{self.nom} avec comme resultat : {self.list_match}"

    def fin_tour(self):
        if self.date_heure_fin is None:
            db = database.get_db_tournoi()
            self.date_heure_fin = datetime.now().strftime("%d/%m/%Y")
            TournoiQuery = Query()
            db.update({"date_fin": self.date_heure_fin}, TournoiQuery.nom == self.date_heure_fin)
            print(f"{str(self)} vient de se finir.")
        else:
            print(f"{str(self)} est déjà terminée.")


if __name__ == "__main__":
    pass