from datetime import date, datetime

from tinydb import TinyDB, Query


class Joueur:
    def __init__(self, nom: str, prenom: str, date_naissance: date, id_echec: str, score:int = 0):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_echec = id_echec
        self.score = score

    def save_joueur(self):
        """
        Accède à la base de donnée joueurs.json.
        Recherche si id du joueur existe, si False rajoute le Joueur à la base de donnée
        :return: None
        """
        path = "../data/joueurs/joueurs.json"
        db = TinyDB(path)
        JoueurQuery = Query()
        if not db.search(JoueurQuery.id_echec == self.id_echec):
            db.insert(dict(self))
            print(str(self) + " ajouter à la base de donnée joueurs.json")
        else:
            print(str(self) + " existe déjà")

    def __iter__(self):
        for key, value in self.__dict__.items():
            if key == "date_naissance" and hasattr(value, "isoformat"):
                yield key, value.isoformat()
            else:
                yield key, value

    def __str__(self):
        return f"{self.id_echec}: {self.nom} {self.prenom}, né le {self.date_naissance}"


if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y").date()
    p = Joueur("test","test",bd, "QZ11122")

    print(dict(p))