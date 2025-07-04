from datetime import date, datetime


class Player:
    def __init__(self, name: str, firstname: str, birthday: date, id_chess: str, score:int = 0):
        self.name = name
        self.firstname = firstname
        self.birthday = birthday
        self.id_chess = id_chess
        self.score = score

    def __iter__(self):
        for key, value in self.__dict__.items():
            if key == "birthday" and hasattr(value, "isoformat"): # pour compatibilité avec tiny DB
                yield key, value.isoformat()
            else:
                yield key, value

    def __repr__(self):
        return f"Joueur: ({self.id_chess}: {self.name} {self.firstname})"

    def __str__(self):
        return f"{self.id_chess}: {self.name} {self.firstname}, né le {self.birthday.strftime("%d/%m/%Y")}"

    def __lt__(self, other):
        """ dunder pour inférieur que """
        if isinstance(other, Player):
            return self.score < other.score

    def __eq__(self, other):
        """ dunder pour egal """
        if isinstance(other, Player):
            return self.score == other.score


if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Player("test", "test", bd, "QZ11122")

