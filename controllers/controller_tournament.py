from utils.database import get_db_tournament
from views.view import View
from controllers.controller_current_tournament import ControllerCurrentTournament

class ControllerTournament:
    def __init__(self):
        self.db = get_db_tournament()
        self.controller_current_tournament = ControllerCurrentTournament()
        self.view = View()

    def run (self):
        """Menu tournoi"""
        title = ("Gestion des tournois\n"
                 "Choisissez une option:")
        option = {
            "Créer un nouveau tournoi": NotImplemented,
            "Modifier un tournoi": NotImplemented,
            "Supprimer un tournoi": NotImplemented,
            "Liste des tournois": NotImplemented,
            "Details d'un tournoi": NotImplemented,
            "Continuez un tournoi existant": self.controller_current_tournament.run,
            "Retour": self.retour
        }
        self.view.menu(title, option)

    def retour(self):
        from controllers.controller_interface import ControllerInterface
        controller = ControllerInterface()
        return controller.run()