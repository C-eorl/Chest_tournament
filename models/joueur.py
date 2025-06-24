from datetime import date
from tinydb import TinyDB


class Joueur:
    def __init__(self, nom: str, prenom: str, date_naissance: date, id_echec: str, score:int = 0):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_echec = id_echec
        self.score = score

    def save_joueur(self):
        path = "../data/joueurs/joueurs.json"
        db = TinyDB(path)
        db.insert(self.to_dict())

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance.isoformat(),
            "id_echec": self.id_echec,
            "score": self.score
        }

    def __str__(self):
        return f"{self.id_echec}: {self.nom} {self.prenom}, né le {self.date_naissance}"


if __name__ == "__main__":
    bd = date(92,1,27)
    p = Joueur("rocher","flo",bd, "SD45678")

