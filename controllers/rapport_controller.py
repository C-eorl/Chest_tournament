from views.view import View
from utils.exit_menu import retour


class ControllerRapport:
    def __init__(self, app_controller):
        self.app = app_controller
        self.view = View()
        self.controller_player = self.app.controller_player

    def run(self):
        """Menu rapport"""
        title = ("Gestion des rapports\n"
                 "Choisissez une option:")
        option = {
            "Liste de tous les joueurs": self.controller_player.list_players,
            "Liste de tous les tournois": NotImplemented,
            "Liste des joueurs du tournoi par ordre alphabétique": NotImplemented,
            "Exporter les rapports": NotImplemented,
            "Retour": retour
        }
        self.view.menu(title, option)