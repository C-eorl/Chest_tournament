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
        """renvoi un dict de l'objet"""
        return {
            "player1": self.player1.to_dict(),
            "player2": self.player2.to_dict(),
            "score1": self.score1,
            "score2": self.score2
        }

    @classmethod
    def from_dict(cls, data):
        """renvoie un objet grâce à un dict"""
        match = cls(
            player1=Player.from_dict(data["player1"]),
            player2=Player.from_dict(data["player2"])
        )
        match.score1 = data.get("score1", 0.0)
        match.score2 = data.get("score2", 0.0)
        return match

    def get_result(self, winner):
        """determine le résultat du match"""
        match winner:
            case self.player1: self.score1 = 1.0
            case self.player2: self.score2 = 1.0
            case "Match nul":
                self.score1 = 0.5
                self.score2 = 0.5

    def tuple_return(self):
        """renvoi un tuple des résultats du match"""
        return ([self.player1, self.score1], [self.player2, self.score2])
