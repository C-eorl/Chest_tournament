import questionary
from rich.console import Console
from rich.table import Table

from models.player import Player
from utils.validation import validate_field
from views.view import View


class ViewPlayer(View):

    def display_modify_player(self, player):
        """
        menu pour modifier le joueur
        :param player: dictionnaire du joueur selectionné
        :return: dict des modifications à changer
        """
        if not player:
            self.display_message(f"Aucun joueur avec cet ID")
            return None

        champs = ["Nom", "prénom", "date de naissance", "id_echec"]
        champs_technique = ["name", "firstname", "birthdate", "id_chess"]

        # Création d'un dictionnaire pour faire le lien entre affichage et clé technique
        mapping = dict(zip(champs, champs_technique))

        champs_a_modifier = questionary.checkbox(
            "Quels champs souhaitez-vous modifier ?",
            choices=champs
        ).ask()

        modifications = {}
        for champ in champs_a_modifier:
            cle_technique = mapping[champ]  # récupère la clé technique correspondante
            valeur_actuelle = getattr(player, cle_technique, "")
            while True:
                nouvelle_valeur = questionary.text(
                    f"Nouvelle valeur pour {champ} (actuel: {valeur_actuelle}) : (laisser vide pour annuler)"
                ).ask()

                if not nouvelle_valeur:  # annulation modification pour ce champ
                    break

                if validate_field(cle_technique, nouvelle_valeur):
                    modifications[cle_technique] = nouvelle_valeur
                    break
                else:
                    print(f"Valeur invalide pour {champ}. Veuillez réessayer.")

            return modifications

    def input_player(self):

        firstname = questionary.text("Prénom :", validate=lambda text: validate_field("firstname", text)).ask()
        if firstname:
            firstname = firstname.capitalize()
        name = questionary.text("Nom :", validate=lambda text: validate_field("name", text)).ask()
        if name:
            name = name.capitalize()
        birthdate = questionary.text("Date de naissance (dd/mm/aaaa) :", validate=lambda text: validate_field("birthdate", text)).ask()
        id_chess = questionary.text("ID national d'échec (ex: AA12345) :", validate=lambda text: validate_field("id_chess", text)).ask()

        return [name, firstname, birthdate, id_chess]