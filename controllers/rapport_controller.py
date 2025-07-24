from views.view import View


class ControllerRapport:
    def __init__(self, app_controller):
        self.app = app_controller
        self.view = View()
        self.controller_player = self.app.controller_player
        self.controller_tournament = self.app.controller_tournament

    def run(self):
        """Menu rapport"""
        title = "Gestion des rapports - Choisissez une option:\n"
        options = {
            "Liste de tous les joueurs": self.controller_player.list_players,
            "Liste de tous les tournois": self.controller_tournament.list_tournaments,
            "Liste des joueurs du tournoi par ordre alphabétique": self.players_in_tournament,
            "Exporter les rapports": NotImplemented,
            "Retour": None
        }
        while True:
            choice = self.view.menu(title, options)
            if choice is None:
                break
            choice()

    def players_in_tournament(self):

        list_tournament = self.controller_tournament.repo_tournament.get_list_tournaments()
        if list_tournament:
            tournament = self.view.display_selected_data(list_tournament)
            title_table= f"Liste des joueurs pour le tournoi {tournament.tournament_name}"
            fields = ["id_chess","name", "firstname", "birthdate"]
            self.view.display_list_data(tournament.list_participant, title_table, fields)
        else:
            self.view.display_message("Aucun tournoi dans la base de donnée")
