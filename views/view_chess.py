import re
import questionary
import rich
from rich.console import Console
from rich.table import Table


class View:
    def menu(self, titre, options):
        """
        Affiche un menu interactif dans le terminal.
        :param titre: Le titre affiché au-dessus des choix.
        :param options: Un dictionnaire où les clés sont les libellés affichés,
                        et les valeurs sont des fonctions à exécuter.
        """
        print("_____________________________________________________")
        choix = questionary.select(
            titre,
            choices=list(options.keys())
        ).ask()
        action = options[choix]
        action()


    def display_message(self, message):
        print(message)

    def input_joueur(self):
        # Validation prénom : pas de chiffres, non vide
        def validate_firstname(text):
            if not text or any(char.isdigit() for char in text):
                return "Le prénom ne doit pas contenir de chiffres et ne peut pas être vide"
            return True
        firstname = questionary.text("Prénom :", validate=validate_firstname).ask()
        if firstname:
            firstname = firstname.capitalize()

        # Validation nom : même règle que prénom
        def validate_name(text):
            if not text or any(char.isdigit() for char in text):
                return "Le nom ne doit pas contenir de chiffres et ne peut pas être vide"
            return True
        name = questionary.text("Nom :", validate=validate_name).ask()
        if name:
            name = name.capitalize()

        # Validation date naissance au format dd/mm/yyyy
        def validate_date(text):
            pattern_date = r"^([0-2][0-9]|3[01])/([0][1-9]|1[0-2])/(\d{4})$"
            if not re.match(pattern_date, text):
                return "Format invalide (dd/mm/aaaa)"
            return True
        birthday = questionary.text("Date de naissance (dd/mm/aaaa) :", validate=validate_date).ask()

        # Validation ID échec (ex: AA12345)
        def validate_id(text):
            pattern_id = r'^[A-Z]{2}\d{5}$'
            if not re.match(pattern_id, text):
                return "Format invalide (ex: AA12345)"
            return True
        id_chess = questionary.text("ID national d'échec (ex: AA12345) :", validate=validate_id).ask()

        return [firstname, name, birthday, id_chess]

    def display_list_players(self, list_players):
        table = Table(title="Liste des joueurs")
        table.add_column("IDN d'échec")
        table.add_column("Nom")
        table.add_column("Prénom")
        table.add_column("Date de naissance")
        for player in list_players:
            table.add_row(player["id_chess"],player["name"],player["firstname"],player["birthday"],)
        console = Console()
        console.print(table)

    def display_modify_player(self, player):

        if not player:
            self.display_message(f"Aucun joueur avec cet ID")
            return None

        champs = ["Nom", "prénom", "date de naissance", "id_echec"]
        champs_technique = ["name", "firstname", "birthday", "id_chess"]

        # Création d'un dictionnaire pour faire le lien entre affichage et clé technique
        mapping = dict(zip(champs, champs_technique))

        champs_a_modifier = questionary.checkbox(
            "Quels champs souhaitez-vous modifier ?",
            choices=champs
        ).ask()

        modifications = {}
        for champ in champs_a_modifier:
            cle_technique = mapping[champ]  # récupère la clé technique correspondante
            valeur_actuelle = player.get(cle_technique, "")
            nouvelle_valeur = questionary.text(f"Nouvelle valeur pour {champ} (actuel: {valeur_actuelle}) :").ask()
            modifications[cle_technique] = nouvelle_valeur

        return modifications

if __name__ == "__main__" :
    pass