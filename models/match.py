from datetime import datetime

from player import Player

class Match:
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.score1 = self.player1.score
        self.player2 = player2
        self.score2 = self.player2.score

    def __iter__(self):
        for key, value in self.__dict__.items():
            if isinstance(value, Player):
                yield key, value
            yield key, value

    def __str__(self):
        return f"{self.player1} - SCORE: {self.player1.score}, {self.player2} - SCORE: {self.player2.score}"

    def result(self):
        return ([self.player1, self.player1.score], [self.player2, self.player2.score])

if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Player("Test", "Test", bd, "QZ11122")
    bd2 = datetime.strptime("15/09/1985", "%d/%m/%Y")
    p2 = Player("Zenzr", "Zerzef", bd, "QZ11122")
    m = Match(p, p2)

    print(m)