from joueur import Joueur

class Match:
    def __init__(self, adversaire: tuple[list[Joueur, int],list[Joueur, int]]):
        self.adversaire = adversaire