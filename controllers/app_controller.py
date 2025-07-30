from controllers.current_tournament_controller import ControllerCurrentTournament
from controllers.player_controller import ControllerPlayer
from controllers.tournament_controller import ControllerTournament
from controllers.rapport_controller import ControllerRapport
from controllers.main_menu_controller import MainMenuController
from utils.database import initialise_data_directories


class AppController:
    def __init__(self):
        self.controller_player = ControllerPlayer(self)
        self.controller_tournament = ControllerTournament(self)
        self.controller_rapport = ControllerRapport(self)
        self.controller_current_tournament = ControllerCurrentTournament(self)
        self.main_menu = MainMenuController(self)

    def run(self):
        """Lance la fonction de départ du memu principal et initialise les dossiers DB"""
        initialise_data_directories()
        self.main_menu.run()
