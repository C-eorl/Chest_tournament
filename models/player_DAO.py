from tinydb import Query


class PlayerRepository:
    def __init__(self, db):
        self.db = db
        self.JoueurQuery = Query()

    def add(self, data):
        """Ajoute un Joueur à la base de donnée"""
        self.db.insert(dict(data))

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
        return self.db.all()