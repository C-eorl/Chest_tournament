from views.view import View


class ControllerCurrentTournament:
    def __init__(self):
        self.view = View()


    def run(self):
        """Menu tournoi en cours"""
        # TODO: liste des tournois en cours + choix
        title = ("Gestion du tournoi en cours\n"
                 "Choisissez une option:")
        option = {
            "Affichage du Round actuel et des matchs": NotImplemented,
            "Saisie des résultats": NotImplemented,
            "Round suivant": NotImplemented,
            "Mettre fin au tournoi": NotImplemented,
            "Retour": self.retour
        }
        self.view.menu(title, option)

    def retour(self):
        from controllers.controller_interface import ControllerInterface
        controller = ControllerInterface()
        return controller.run()