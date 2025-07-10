from datetime import datetime
import questionary
from utils.exit_menu import retour
from models.player import Player
from views.view_player import ViewPlayer
from utils.database import get_db_player
from models.player_DAO import PlayerRepository


class ControllerPlayer:
    def __init__(self):
        self.view = ViewPlayer()
        self.db = get_db_player()
        self.repo_player = PlayerRepository(self.db)


    def run(self):
        """Menu joueur"""
        title = ("Gestion des joueurs\n"
                 "Choisissez une option:")
        option = {
            "Ajouter un joueur": self.registration_player,
            "Modifier un joueur": self.modify_player,
            "Liste des joueurs": self.list_players,
            "Retour": retour
        }
        self.view.menu(title, option)

    def get_player(self) -> Player:
        """
        Récupère les données transmisent par l'utilisateur, transforme la date
        :return: Player avec les données utilisateur
        """
        info_player = self.view.input_player()
        info_player[2] = datetime.strptime(info_player[2], "%d/%m/%Y").date()

        return Player(info_player[0], info_player[1], info_player[2], info_player[3])

    def save(self, player : Player):
        """
        sauvegarde le joueur dans la base de donnée
        :param player : un objet Joueur
        :return: True si le joueur n'existe pas et le rajoute à la base de donnée, False s'il existe
        """
        if not self.repo_player.search(player.id_chess):
            self.repo_player.add(player)
            return True
        return False

    def registration_player(self):
        """
        Récupère un object Joueur et appelle la fonction save() pour enregistrer le Joueur, affiche un message.
        :return: None
        """
        joueur = self.get_player()
        if self.save(joueur):
            self.view.display_message(f"{str(joueur)} a été ajouté à la base de donnée")
        else:
            self.view.display_message(f"{str(joueur)} existe déjà dans la base de donnée")

    def list_players(self):
        """
        récupere la liste complète des joueurs
        :return: dict de tous les joueurs
        """
        list_players = self.repo_player.get_list_players()
        sorted_list_player = sorted(list_players, key=lambda x: x.name)
        self.view.display_list_data(sorted_list_player, "Liste des joueurs", ["id_chess","name", "firstname", "birthdate"])

    def modify_player(self):
        """
        Récupère Id_chess du choix utilisateur pour chercher le joueur associé.
        Demande la modification puis mets à jour le joueur dans la base de donnée
        :return: None
        """
        self.view.display_message("Quel joueur voulez-vous modifier : ")
        players = self.repo_player.get_list_players()
        choices = [
            questionary.Choice(
                title=f"{player}",
                value=player
            )
            for player in players
        ]

        player_selectionne = questionary.select(
            "Sélectionnez un joueur (filtrable) :",
            choices=choices,
            use_search_filter=True,
            use_jk_keys=False
        ).ask()
        modifications = self.view.display_modify_player(player_selectionne)
        print(modifications)
        if modifications:
            self.repo_player.update(player_selectionne.id_chess, modifications)
            self.view.display_message("Joueur modifié avec succès.")
        else:
            self.view.display_message("Aucune modification effectuée.")


if __name__ == "__main__":
    pass