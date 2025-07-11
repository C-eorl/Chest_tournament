from views.view_player import ViewPlayer
from controllers.controller_player import ControllerPlayer
from controllers.controller_tournament import ControllerTournament
from controllers.controller_current_tournament import ControllerCurrentTournament
from controllers.controller_rapport import ControllerRapport
from utils.decorateur_try import decorator_try

class ControllerInterface:
    def __init__(self):
        self.controller_player = ControllerPlayer()
        self.controller_tournament = ControllerTournament()
        self.controller_current_tournament = ControllerCurrentTournament()
        self.controller_rapport = ControllerRapport()
        self.view = ViewPlayer()

    @decorator_try
    def run(self):
        """Menu principal"""

        title = ("Chess Tournament manager\n"
                "Choisissez une option:")
        # condition "continuez tournoi" affiché si tournoi en cours
        option = {
            "Joueurs": self.controller_player.run,
            "Tournois": self.controller_tournament.run,
            "Continuez un tournoi existant": self.controller_current_tournament.run,
            "Rapports": self.controller_rapport.run,
            "Quittez": exit
        }
        exist_current = self.controller_current_tournament.list_current_tournament()
        if not exist_current:
            option.pop("Continuez un tournoi existant")
        self.view.menu(title, option)


if __name__ == "__main__":
    pass