from tinydb import Query, where
from models.tournament import Tournament


class TournamentRepository:
    def __init__(self, db):
        self.db = db
        self.TournamentQuery = Query()

    def add(self, tournament: Tournament):
        """Ajoute un Tournoi à la base de donnée"""
        self.db.insert(tournament.to_dict())

    def search(self, name: str) -> dict | None:
        """Recherche un tournoi grâce à son name"""
        return self.db.search(self.TournamentQuery.name == name)

    def search_is(self, statut: str) -> dict | None:
        """Recherche un tournoi grâce à son statut"""
        return self.db.search(where("statut") == statut)

    def update(self, name: str, valeur: dict):
        """
        Mets à jour les informations d'un tournoi
        :param name: nom du tournoi
        :param valeur: valeurs modifiées
        :return: None
        """
        self.db.update(valeur, self.TournamentQuery.tournament_name == name)

    def get_list_tournaments(self):
        """Renvoie la liste de tous les tournois"""
        tournaments_data = self.db.all()
        return [Tournament.from_dict(tournament) for tournament in tournaments_data]

    def delete_tournament(self, tournament):
        """Supprime un tournoi"""
        self.db.remove(where("tournament_name") == tournament.tournament_name)
