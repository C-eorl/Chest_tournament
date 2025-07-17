from utils.decorateur_try import decorator_try
from views.view import View

class MainMenuController:
    def __init__(self, app_controller):
        self.app = app_controller
        self.view = View()

    @decorator_try
    def run(self):
        """Affiche le menu principal"""
        title = "Chess Tournament manager\nChoisissez une option :"
        options = {
            "Joueurs": self.app.controller_player.run,
            "Tournois": self.app.controller_tournament.run,
            "Continuez un tournoi existant": self.app.controller_current_tournament.run,
            "Rapports": self.app.controller_rapport.run,
            "Quittez": exit
        }

        exist_current = self.app.controller_current_tournament.list_current_tournament()
        if not exist_current:
            options.pop("Continuez un tournoi existant")
        self.view.menu(title, options)
