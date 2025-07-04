from datetime import date, datetime
from utils.database import PlayerRepository, get_db_player


class Joueur:
    def __init__(self, nom: str, prenom: str, date_naissance: date, id_echec: str, score:int = 0):
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.id_echec = id_echec
        self.score = score

    def __iter__(self):
        for key, value in self.__dict__.items():
            if key == "date_naissance" and hasattr(value, "isoformat"): # pour compatibilité avec tiny DB
                yield key, value.isoformat()
            else:
                yield key, value

    def __repr__(self):
        return f"Joueur: ({self.id_echec}: {self.nom} {self.prenom})"

    def __str__(self):
        return f"{self.id_echec}: {self.nom} {self.prenom}, né le {self.date_naissance.strftime("%d/%m/%Y")}"

    def __lt__(self, other):
        """ dunder pour inférieur que """
        if isinstance(other, Joueur):
            return self.score < other.score

    def __eq__(self, other):
        """ dunder pour egal """
        if isinstance(other, Joueur):
            return self.score == other.score

    def save(self, repo: PlayerRepository):
        """
        sauvegarde le joueur dans la base de donnée
        :param repo: class manageur de joueur
        :return: True si le joueur n'existe pas et le rajoute à la base de donnée, False s'il existe
        """
        if not repo.player_exist(self.id_echec):
            repo.add_db(self)
            return True
        return False


if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Joueur("test","test",bd, "QZ11122")
    db = get_db_player()
    repo_player = PlayerRepository(db)
    p.save(repo_player)

