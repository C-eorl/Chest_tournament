import json
import re
from datetime import datetime

from models.joueur import Joueur
from views.view_chess import View


class Controler:
    def __init__(self):
        self.view = View()



    def ajouter_joueur(self):
        info_joueur = self.view.input_joueur()
        info_joueur[2] = datetime.strptime(info_joueur[2], "%d/%m/%Y").date()

        return Joueur(info_joueur[0], info_joueur[1], info_joueur[2], info_joueur[3])

    def enregistrement_joueur(self):
        joueur = self.ajouter_joueur()
        joueur.save_joueur()



if __name__ == "__main__":
    c = Controler()
    c.enregistrement_joueur()