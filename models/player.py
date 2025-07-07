from datetime import date, datetime

# patern model façade
class Player:
    def __init__(self, name: str, firstname: str, birthdate: date, id_chess: str, score:int = 0):
        self.name = name
        self.firstname = firstname
        self.birthdate = birthdate
        self.id_chess = id_chess
        self.score = score



    def __repr__(self):
        return f"Joueur: ({self.id_chess}: {self.name} {self.firstname})"

    def __str__(self):
        return f"{self.id_chess}: {self.name} {self.firstname}, né le {self.birthdate.strftime("%d/%m/%Y")}"

    def __lt__(self, other):
        """ dunder pour inférieur que """
        if isinstance(other, Player):
            return self.score < other.score

    def __eq__(self, other):
        """ dunder pour egal """
        if isinstance(other, Player):
            return self.score == other.score

    def to_dict(self):
        return {
            'name': self.name,
            'firstname': self.firstname,
            'birthdate': self.birthdate.strftime("%d/%m/%Y"),
            'id_chess': self.id_chess
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            name = data["name"],
            firstname = data["firstname"],
            birthdate=datetime.strptime(data["birthdate"], "%Y/%m/%d").date(),
            id_chess = data["id_chess"],
        )

if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Player("test", "test", bd, "QZ11122")

    bd.strptime()