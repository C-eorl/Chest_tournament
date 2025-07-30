from datetime import datetime
from utils.decorateur_try import decorator_try
from models.player import Player
from views.view_player import ViewPlayer
from utils.database import get_db_player
from models.player_DAO import PlayerRepository


class ControllerPlayer:
    def __init__(self, app_controller):
        self.app = app_controller
        self.view = ViewPlayer()
        self.db = get_db_player()
        self.repo_player = PlayerRepository(self.db)

    @decorator_try
    def run(self):
        """Menu joueur"""
        title = "Gestion des joueurs - Choisissez une option:\n"
        options = {
            "Ajouter un joueur": self.registration_player,
            "Modifier un joueur": self.modify_player,
            "Liste des joueurs": self.list_players,
            "Retour": None
        }

        while True:
            choice = self.view.menu(title, options)
            if choice is None:
                break
            choice()

    def get_player(self) -> Player | None:
        """
        Récupère les données transmises par l'utilisateur, transforme la date de naissance en objet Datetime
        :return: Player avec les données utilisateur sinon None
        """

        info_player = self.view.input_player()
        if None not in info_player:
            info_player[2] = datetime.strptime(info_player[2], "%d/%m/%Y").date()
            return Player(info_player[0], info_player[1], info_player[2], info_player[3])
        else:
            return None

    def save(self, player: Player):
        """
        sauvegarde le joueur dans la base de donnée
        :param player : un objet Player
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
        player = self.get_player()
        if player is None:
            self.view.display_message("Annulation de la saisie du joueur, information manquante")
            self.view.display_message("Le joueur n'a pas pu être ajouté à la base de donnée")
        else:
            if self.save(player):
                self.view.display_message(f"{str(player)} a été ajouté à la base de donnée")
            else:
                self.view.display_message(f"L'ID {player.id_chess} est déjà utilisé")

    def list_players(self):
        """
        récupère la liste complète des joueurs, la trie et l'affiche
        """
        list_players = self.repo_player.get_list_players()
        sorted_list_player = sorted(list_players, key=lambda x: x.name)
        self.view.display_list_data(
            sorted_list_player,
            "Liste des joueurs",
            ["id_chess", "name", "firstname", "birthdate"]
        )

    def modify_player(self):
        """
        Récupère Id_chess du choix utilisateur pour chercher le joueur associé.
        Demande la modification puis mets à jour le joueur dans la base de donnée
        :return: None
        """
        self.view.separator()
        self.view.display_message("Quel joueur voulez-vous modifier ? ")
        players = self.repo_player.get_list_players()
        player_selected = self.view.display_selected_data(players)
        if not player_selected:
            self.view.display_message("Annulation de la modification du joueur")
            return
        fields = ["Nom", "prénom", "date de naissance"]
        technic_fields = ["name", "firstname", "birthdate"]
        modifications = self.view.display_modify_data(player_selected, fields, technic_fields)

        if not modifications:
            self.view.display_message("Aucune modification effectuée.")
        else:
            for key, value in modifications.items():
                if key in ("name", "firstname"):
                    modifications[key] = value.capitalize()
            self.repo_player.update(player_selected.id_chess, modifications)
            self.view.display_message("Joueur modifié avec succès.")
