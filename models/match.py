from datetime import datetime
from models.player import Player

class Match:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.score1 = 0.0
        self.score2 = 0.0

    def __repr__(self):
        return f"{self.player1} contre {self.player2}"

    def __str__(self):
        return f"{self.player1.simple_str()} contre {self.player2.simple_str()}"

    def to_dict(self):
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2
        }

    @classmethod
    def from_dict(cls, data):
        match= cls(
            player1=Player.from_dict(data["player1"]),
            player2=Player.from_dict(data["player2"])
        )
        match.score1 = data.get("score1", 0.0)
        match.score2 = data.get("score2", 0.0)
        return match

    def get_result(self, winner):
        match winner:
            case self.player1: self.score1 = 1.0
            case self.player2: self.score2 = 1.0
            case "Match nul":
                self.score1 = 0.5
                self.score2 = 0.5

    def tuple_return(self):
        return ([self.player1, self.score1], [self.player2, self.score2])

if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Player("Test", "Test", bd, "QZ11122")
    bd2 = datetime.strptime("15/09/1985", "%d/%m/%Y")
    p2 = Player("Zenzr", "Zerzef", bd, "QZ11122")
    m = Match(p, p2)

    print(m)