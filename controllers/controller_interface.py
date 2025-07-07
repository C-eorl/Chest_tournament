from views.view_chess import View
from controllers.controller_player import ControllerPlayer

class ControllerInterface:
    def __init__(self):
        self.controller_player = ControllerPlayer()
        self.view = View()

    def main_menu(self):
        """Menu principal"""
        title = ("Chess Tournament manager\n"
                "Choisissez une option:")
        # condition "continuez tournoi" affiché si tournoi en cours
        option = {
            "Joueurs": self.player_menu,
            "Tournois": self.tournament_menu,
            "Continuez un tournoi existant": self.current_tournament_menu,
            "Rapports": self.rapport_menu,
            "Quittez": exit
        }
        self.view.menu(title, option)

    def player_menu(self):
        """Menu joueur"""
        title = ("Gestion des joueurs\n"
                 "Choisissez une option:")
        option = {
            "Ajouter un joueur": self.controller_player.registration_player,
            "Modifier un joueur": self.controller_player.modify_player,
            "Liste des joueurs": self.controller_player.list_players,
            "Retour": self.main_menu
        }
        self.view.menu(title, option)

    def tournament_menu(self):
        """Menu tournoi"""
        title = ("Gestion des tournois\n"
                 "Choisissez une option:")
        option = {
            "Créer un nouveau tournoi": NotImplemented,
            "Modifier un tournoi": NotImplemented,
            "Supprimer un tournoi": NotImplemented,
            "Liste des tournois": NotImplemented,
            "Details d'un tournoi": NotImplemented,
            "Continuez un tournoi existant": self.current_tournament_menu,
            "Retour": self.main_menu
        }
        self.view.menu(title, option)

    def current_tournament_menu(self):
        """Menu tournoi en cours"""
        # TODO: liste des tournois en cours + choix
        title = ("Gestion du tournoi en cours\n"
                 "Choisissez une option:")
        option = {
            "Affichage du Round actuel et des matchs": NotImplemented,
            "Saisie des résultats": NotImplemented,
            "Round suivant": NotImplemented,
            "Mettre fin au tournoi": NotImplemented,
            "Retour": self.main_menu
        }
        self.view.menu(title, option)

    def rapport_menu(self):
        """Menu rapport"""
        title = ("Gestion des rapports\n"
                 "Choisissez une option:")
        option = {
            "Liste de tous les joueurs": NotImplemented,
            "Liste de tous les tournois": NotImplemented,
            "Liste des joueurs du tournoi par ordre alphabétique": NotImplemented,
            "Retour": self.main_menu
        }
        self.view.menu(title, option)




if __name__ == "__main__":
    c = ControllerPlayer()
    print(c.db.all())
    player = c.repo_player.player_search("HJ45612")
    print(player)