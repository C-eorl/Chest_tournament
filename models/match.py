from datetime import datetime

from joueur import Joueur

class Match:
    def __init__(self, joueur1: Joueur, joueur2: Joueur):
        self.joueur1 = joueur1
        self.score1 = self.joueur1.score
        self.joueur2 = joueur2
        self.score2 = self.joueur2.score

    def __iter__(self):
        for key, value in self.__dict__.items():
            if isinstance(value, Joueur):
                yield key, value
            yield key, value

    def __str__(self):
        return f"{self.joueur1} - SCORE: {self.joueur1.score}, {self.joueur2} - SCORE: {self.joueur2.score}"

    def resultat(self):
        return ([self.joueur1, self.joueur1.score], [self.joueur2, self.joueur2.score])

if __name__ == "__main__":
    bd = datetime.strptime("01/11/1945", "%d/%m/%Y")
    p = Joueur("Test", "Test", bd, "QZ11122")
    bd2 = datetime.strptime("15/09/1985", "%d/%m/%Y")
    p2 = Joueur("Zenzr", "Zerzef", bd, "QZ11122")
    m = Match(p, p2)

    print(m)