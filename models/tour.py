from datetime import datetime

from tinydb import Query

from match import Match
from utils import database


class Tour:
    def __init__(self, list_match: list[Match], name: str, date_time_end):
        self.list_match = list_match
        self.name = name
        self.date_time_start = datetime.now()
        self.date_time_end = date_time_end

    def __str__(self):
        return f"{self.name} avec comme resultat : {self.list_match}"

    def finished_tour(self):
        if self.date_time_end is None:
            db = database.get_db_tournoi()
            self.date_time_end = datetime.now().strftime("%d/%m/%Y")
            TournoiQuery = Query()
            db.update({"date_fin": self.date_time_end}, TournoiQuery.nom == self.date_time_end)
            print(f"{str(self)} vient de se finir.")
        else:
            print(f"{str(self)} est déjà terminée.")


if __name__ == "__main__":
    pass