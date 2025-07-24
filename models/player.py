from datetime import date, datetime


class Player:
    def __init__(self, name: str, firstname: str, birthdate: date, id_chess: str):
        self.name = name
        self.firstname = firstname
        self.birthdate = birthdate
        self.id_chess = id_chess

    def __repr__(self):
        return f"Joueur: ({self.id_chess}: {self.name} {self.firstname})"

    def __str__(self):
        return f"{self.id_chess}: {self.name} {self.firstname}, né le {self.birthdate.strftime('%d/%m/%Y')}"

    def simple_str(self):
        return f"{self.id_chess}: {self.name} {self.firstname}"

    def __hash__(self):
        return hash(self.id_chess)

    def __eq__(self, other):
        """ dunder pour egal """
        if not isinstance(other, Player):
            return False
        return self.id_chess == other.id_chess

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
            name=data["name"],
            firstname=data["firstname"],
            birthdate=datetime.strptime(data["birthdate"], "%d/%m/%Y").date(),
            id_chess=data["id_chess"],
        )


if __name__ == "__main__":
    pass
