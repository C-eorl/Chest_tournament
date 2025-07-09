from views.view import View
from controllers.controller_player import ControllerPlayer


class ControllerRapport:
    def __init__(self):
        self.view = View()
        self.controller_player = ControllerPlayer()

    def run(self):
        """Menu rapport"""
        title = ("Gestion des rapports\n"
                 "Choisissez une option:")
        option = {
            "Liste de tous les joueurs": self.controller_player.list_players,
            "Liste de tous les tournois": NotImplemented,
            "Liste des joueurs du tournoi par ordre alphabétique": NotImplemented,
            "Exporter les rapports": NotImplemented,
            "Retour": self.retour
        }
        self.view.menu(title, option)

    def retour(self):
        from controllers.controller_interface import ControllerInterface
        controller = ControllerInterface()
        return controller.run()