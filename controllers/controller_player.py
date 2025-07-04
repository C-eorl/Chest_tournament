from datetime import datetime
from random import choices

import questionary

from models.player import Player
from views.view_chess import View
from utils.database import get_db_player, PlayerRepository


class ControllerPlayer:
    def __init__(self):
        self.view = View()
        self.db = get_db_player()
        self.repo = PlayerRepository(self.db)

    def get_player(self) -> Player:
        """
        Récupère les données transmisent par l'utilisateur, transforme la date
        :return: Player avec les données utilisateur
        """
        info_player = self.view.input_joueur()
        info_player[2] = datetime.strptime(info_player[2], "%d/%m/%Y").date()

        return Player(info_player[0], info_player[1], info_player[2], info_player[3])

    def save(self, player : Player):
        """
        sauvegarde le joueur dans la base de donnée
        :param repo: class manageur de joueur
        :return: True si le joueur n'existe pas et le rajoute à la base de donnée, False s'il existe
        """
        if not self.repo.player_exist(player.id_chess):
            self.repo.add_db(player)
            return True
        return False

    def registration_player(self):
        """
        Récupère un object Joueur et appelle la fonction save() pour enregistrer le Joueur, affiche un message.
        :return: None
        """
        joueur = self.get_player()
        if self.save(joueur):
            self.view.display_message(f"{str(joueur)} a été ajouté la base de donnée")
        else:
            self.view.display_message(f"{str(joueur)} existe déjà dans la base de donnée")

    def list_players(self):
        """
        récupere la liste complète des joueurs
        :return: dict de tous les joueurs
        """
        list_players = self.repo.get_list_players()
        sorted_list_player = sorted(list_players, key=lambda x: x["name"])
        self.view.display_list_players(sorted_list_player)

    def modify_menu(self):
        """
        récupere l'id d'échec d'un joueur, recherche le joueur, demande quelle modification
        :return:
        """
        self.view.display_message("Quel joueur voulez-vous modifier (par ID nationnal d'échec): ")
        id_player = questionary.text("Id :").ask()
        player = self.repo.player_search(id_player)
        modifications = self.view.display_modify_player(player)

        if modifications:
            self.repo.update_player(id_player, modifications)
            self.view.display_message("Joueur modifié avec succès.")
        else:
            self.view.display_message("Aucune modification effectuée.")

    def alt_modify_player(self):
        self.view.display_message("Quel joueur voulez-vous modifier (par ID nationnal d'échec): ")
        players = self.repo.get_list_players()
        choices = [
            questionary.Choice(
                title=f"{player['firstname']} {player['name']} (ID: {player['id_chess']})",
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
            self.repo.update_player(player_selectionne["id_chess"], modifications)
            self.view.display_message("Joueur modifié avec succès.")
        else:
            self.view.display_message("Aucune modification effectuée.")
if __name__ == "__main__":
    pass