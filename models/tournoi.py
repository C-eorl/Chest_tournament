from datetime import datetime

from tinydb import Query

from models.joueur import Joueur
from utils import database


class Tournoi:
    def __init__(self, nom: str, lieu: str, description: str, nombre_tours: int =4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = datetime.now().strftime("%d/%m/%Y")
        self.date_fin = None
        self.nombre_tours = nombre_tours
        self.description = description
        self.liste_participant = []

    def __str__(self):
        return (f"Tournoi {self.nom} à {self.lieu} (Début: {self.date_debut} - Fin: {self.date_fin})")

    def __iter__(self):
        for key, value in self.__dict__.items():
            yield key, value

    def ajout_participant(self, joueur: Joueur):
        """ Ajoute un Joueur au tournoi """
        self.liste_participant.append(joueur)

    def save_tournoi(self):
        """ Sauvegarde le tournoi dans le fichier tournois.json """
        db = database.get_db_tournoi()
        TournoiQuery = Query()
        if not db.search(TournoiQuery.nom == self.nom):
            db.insert(dict(self))
            print(str(self) + " ajouter à la base de donnée tournois.json")
        else:
            print(str(self) + " existe déjà")

    def tournoi_fini(self):
        """
        Défini date et heure de la fin du tournoi et enregistre la modification dans la base de donnée
        :return: None
        """
        if self.date_fin is None:
            db = database.get_db_tournoi()
            self.date_fin = datetime.now().strftime("%d/%m/%Y")
            TournoiQuery = Query()
            db.update({"date_fin": self.date_fin}, TournoiQuery.nom == self.nom)
            print(f"{str(self)} vient de se finir.")
        else:
            print(f"{str(self)} est déjà terminée.")



if __name__ == "__main__":
    t = Tournoi("t","Bourges","lorem ipsum")
    t.tournoi_fini()
    t.tournoi_fini()