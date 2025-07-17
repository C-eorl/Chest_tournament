from utils.decorateur_try import decorator_try
from utils.exit_menu import retour
from utils.database import get_db_tournament, get_db_player
from views.view_tournament import ViewTournament
from models.tournament import Tournament
from models.tournament_DAO import TournamentRepository
from models.player_DAO import PlayerRepository

class ControllerTournament:
    def __init__(self, app_controller):
        self.app = app_controller
        self.db_player = get_db_player()
        self.repo_player = PlayerRepository(self.db_player)
        self.db = get_db_tournament()
        self.repo_tournament = TournamentRepository(self.db)
        self.view = ViewTournament()

    @decorator_try
    def run (self):
        """Menu tournoi"""
        title = ("Gestion des tournois\n"
                 "Choisissez une option:")
        option = {
            "Créer un nouveau tournoi": self.registration,
            "Démarrer un tournoi": self.start_tournament,
            "Ajouter un participant": self.add_participant_to_tournament,
            "Modifier un tournoi": self.modify_tournament,
            "Supprimer un tournoi": self.delete_tournament,
            "Liste des tournois": self.list_tournaments,
            "Details d'un tournoi": self.detail_tournament,
            "Continuez un tournoi existant": self.app.controller_current_tournament.run,
            "Retour": retour
        }
        exist_current = self.app.controller_current_tournament.list_current_tournament()
        if not exist_current:
            option.pop("Continuez un tournoi existant")
        self.view.menu(title, option)

    def get_tournament(self):
        """Récupère et renvoie les entrées de l'utilisateur """
        info_tournament= self.view.input_tournament()

        return Tournament(*info_tournament)

    def save(self, tournament: Tournament):
        """
        sauvegarde le tournoi dans la base de donnée
        :param tournament : un objet Tournoi
        :return: True si le tournoi n'existe pas et le rajoute à la base de donnée, False s'il existe
        """
        if not self.repo_tournament.search(tournament.tournament_name):
            self.repo_tournament.add(tournament)
            return True
        return False

    def registration(self):
        """Récupère l'objet Tournament pour le sauvegarder dans la base de donnée"""
        tournament = self.get_tournament()
        if self.save(tournament):
            self.view.display_message(f"{str(tournament)} a été ajouté à la base de donnée")
        else:
            self.view.display_message(f"{str(tournament)} existe déjà dans la base de donneé")

    def list_tournaments(self):
        """Récupère la list[Tournament] de tous les tournois et appelle fonction view pour afficher """
        list_tournaments = self.repo_tournament.get_list_tournaments()
        if list_tournaments:
            self.view.display_list_data(list_tournaments, "Liste des tournois", ["tournament_name", "locality", "start_date", "end_date", "statut"])
        else:
            self.view.display_message("Aucun tournoi dans la base de donnée")

    def get_list_ready_tournament(self) -> list[Tournament]:
        """
        Récupère la liste de tous les tournois avec le statut = "ready"
        :return: list[Tournament]
        """
        tournament_current = self.repo_tournament.search_is("ready")
        return [Tournament.from_dict(current) for current in tournament_current]

    def start_tournament(self):
        """
        Récupère la liste des tournois pret, demande à l'utilisateur de sélectionner un tournoi.
        Change le statut du tournoi sélectionné, le mets à jour dans la base de donnée.
        Puis lance le menu Tournoi en cours.
        """
        list_ready_tournament = self.get_list_ready_tournament()
        if list_ready_tournament:
            tournament = self.view.display_selected_tournament(list_ready_tournament)
            tournament.statut = "current"
            self.repo_tournament.update(tournament.tournament_name, tournament.to_dict())
            self.app.controller_current_tournament.target = tournament
            self.add_participant_to_tournament(self.app.controller_current_tournament.target)
            self.app.controller_current_tournament.run()
        else:
            self.view.display_message("pas de tournoi à commencer")

    def modify_tournament(self):
        """
        Récupère la liste de tous les tournois affiche la liste avec option selection puis demande quels champs
        modifier.
        Récupère la modification et met à jour la base de donnée
        :return: None
        """
        self.view.display_message("Quel tournoi voulez-vous modifier ?")
        tournaments = self.repo_tournament.get_list_tournaments()
        tournament_selected = self.view.display_selected_data(tournaments)
        fields = ["Nom", "Ville", "Date de début", "Date de fin", "Nombre de round", "Description", "Statut"]
        technic_fields = ["tournament_name", "locality", "start_date", "end_date", "round_number", "description", "statut"]
        modifications = self.view.display_modify_data(tournament_selected, fields, technic_fields)

        if modifications:
            self.repo_tournament.update(tournament_selected.tournament_name, modifications)
            self.view.display_message("Tournoi modifié avec succès.")
        else:
            self.view.display_message("Aucune modification effectuée.")

    def delete_tournament(self):
        """Supprime un tournoi de la base de donnée"""
        list_tournaments = self.repo_tournament.get_list_tournaments()
        tournament_selected = self.view.display_selected_tournament(list_tournaments)
        self.repo_tournament.delete_tournament(tournament_selected)
        self.view.display_message(f"{tournament_selected} a été supprimé de la base de donnée")

    def detail_tournament(self):
        """Affiche les détails d'un tournoi """
        list_tournaments = self.repo_tournament.get_list_tournaments()
        tournament_selected = self.view.display_selected_tournament(list_tournaments)
        self.view.display_tournament(tournament_selected)

    def add_participant(self):
        """Ajoute des participants à un tournoi choisi par l'utilisateur"""
        list_tournaments = self.repo_tournament.get_list_tournaments()
        tournament_selected = self.view.display_selected_tournament(list_tournaments)
        self.add_participant_to_tournament(tournament_selected)

    def add_participant_to_tournament(self, tournament: Tournament):
        """Rajoute un ou plusieurs joueurs dans un tournoi donné"""
        players = self.repo_player.get_list_players()
        players_selected = self.view.display_checkbox_data(players)

        for player_selected in players_selected:
            if player_selected not in tournament.list_participant:
                tournament.list_participant.append(player_selected)
                self.view.display_message(
                    f"{player_selected} a été rajouté comme participant au tournoi {tournament.tournament_name}")
            else:
                self.view.display_message(
                    f"{player_selected} est déjà inscrit au tournoi {tournament.tournament_name}")

        self.repo_tournament.update(tournament.tournament_name, tournament.to_dict())
