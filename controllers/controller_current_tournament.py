from models.tournament import Tournament
from models.tournament_DAO import TournamentRepository
from utils.database import get_db_tournament
from utils.exit_menu import retour
from views.view_tournament import ViewTournament

class ControllerCurrentTournament:
    def __init__(self):
        self.view = ViewTournament()
        self.db = get_db_tournament()
        self.repo_tournament = TournamentRepository(self.db)
        self.target = None

    def run(self):
        """Menu tournoi en cours"""
        if self.target is None:
            self.target = self.get_tournament_target()
        title = ("Gestion du tournoi en cours\n"       # ajouter f{self target} au titre avec style 
                 "Choisissez une option:")
        option = {
            "Affichage du Round actuel et des matchs": NotImplemented,
            "Saisie des résultats": NotImplemented,
            "Round suivant": NotImplemented,
            "Mettre fin au tournoi": self.finished_tournament,
            "Changez de tournoi en cours": NotImplemented,
            "Retour": retour
        }
        self.view.menu(title, option)


    def finished_tournament(self):
        """Définit le tournoi comme fini et met a jour la base de donnée"""
        self.target.statut = "finished"
        self.repo_tournament.update(self.target.tournament_name, self.target.to_dict())
        self.view.display_message("le tournoi est terminé")
        retour()

    def list_current_tournament(self):
        """retourne une liste de tous les tournois en cours"""
        return [Tournament.from_dict(tournoi) for tournoi in self.repo_tournament.search_is("current")]

    def get_tournament_target(self):
        """renvoie le tournoi en cours ciblé pour l'utiliser"""
        current_tournaments = self.list_current_tournament()
        return self.view.display_tournament(current_tournaments)



