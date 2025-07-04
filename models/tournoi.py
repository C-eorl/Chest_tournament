from datetime import datetime

from tinydb import Query

from models.player import Player
from utils import database


class Tournoi:
    def __init__(self, name: str, locality: str, description: str, round_number: int =4):
        self.name = name
        self.locality = locality
        self.start_date = datetime.now().strftime("%d/%m/%Y")
        self.end_date = None
        self.round_number = round_number
        self.description = description
        self.list_participant = []

    def __str__(self):
        return f"Tournoi {self.name} à {self.locality} (Début: {self.start_date} - Fin: {self.end_date})"

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def ajout_participant(self, joueur: Player):
        """ Ajoute un Joueur au tournoi """
        self.list_participant.append(joueur)

    def save_tournoi(self):
        """ Sauvegarde le tournoi dans le fichier tournois.json """
        db = database.get_db_tournament()
        TournoiQuery = Query()
        if not db.search(TournoiQuery.nom == self.name):
            db.insert(dict(self))
            print(str(self) + " ajouter à la base de donnée tournois.json")
        else:
            print(str(self) + " existe déjà")

    def finished_tournament(self):
        """
        Défini date et heure de la fin du tournoi et enregistre la modification dans la base de donnée
        :return: None
        """
        if self.end_date is None:
            db = database.get_db_tournament()
            self.end_date = datetime.now().strftime("%d/%m/%Y")
            TournoiQuery = Query()
            db.update({"date_fin": self.end_date}, TournoiQuery.nom == self.name)
            print(f"{str(self)} vient de se finir.")
        else:
            print(f"{str(self)} est déjà terminée.")



if __name__ == "__main__":
    t = Tournoi("t","Bourges","lorem ipsum")
