from tinydb import Query
from models.player import Player


class PlayerRepository:
    def __init__(self, db):
        # initialisation db ici
        self.db = db
        self.JoueurQuery = Query()

    def add(self, player: Player ):
        """Ajoute un Joueur à la base de donnée"""
        self.db.insert(player.to_dict())

    def search(self, id_chess) -> dict | None:
        """ Recherche un joueur grâce à son id_chess"""
        return self.db.get(self.JoueurQuery.id_chess == id_chess)

    def update(self, id_chess: str, valeur: dict):
        """
        Mets à jour la base de donnée
        :param id_chess: identifiant échec du joueur
        :param valeur: dict des changements (key: valeur)
        :return: None
        """
        self.db.update(valeur, self.JoueurQuery.id_chess == id_chess)

    def get_list_players(self):
        """Renvoie la liste de tous les joueurs"""
        players_data = self.db.all()
        return [Player.from_dict(player) for player in players_data]