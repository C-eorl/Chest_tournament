from utils.exit_menu import retour
from utils.database import get_db_tournament
from views.view_tournament import ViewTournament
from controllers.controller_current_tournament import ControllerCurrentTournament
from models.tournament import Tournament
from models.tournament_DAO import TournamentRepository

class ControllerTournament:
    def __init__(self):
        self.db = get_db_tournament()
        self.repo_tournament = TournamentRepository(self.db)
        self.controller_current_tournament = ControllerCurrentTournament()
        self.view = ViewTournament()

    def run (self):
        """Menu tournoi"""
        title = ("Gestion des tournois\n"
                 "Choisissez une option:")
        option = {
            "Créer un nouveau tournoi": self.registration,
            "Démarrer un tournoi": self.start_tournament,
            "Modifier un tournoi": NotImplemented,
            "Supprimer un tournoi": NotImplemented,
            "Liste des tournois": self.list_tournaments,
            "Details d'un tournoi": NotImplemented,
            "Continuez un tournoi existant": self.controller_current_tournament.run,
            "Retour": retour
        }
        exist_current = self.controller_current_tournament.list_current_tournament()
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
            tournament = self.view.display_tournament(list_ready_tournament)
            tournament.statut = "current"
            self.repo_tournament.update(tournament.tournament_name, tournament.to_dict())
            self.controller_current_tournament.target = tournament
            self.controller_current_tournament.run()
        else:
            self.view.display_message("pas de tournoi à commencer")
