import questionary

from rich.table import Table
from rich.console import Console
from utils.validation import validate_field


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
        """ Affiche un message
        :param message: str
        """
        print(message)

    def display_error(self, error):
        """
        Affiche l'erreur
        :param error: str
        """
        print(f"Error: {error}")

    def display_list_data(self, list_data: list, title_table: str, fields: list):
        """
        Affiche un tableau avec les données passée (Player, Tournament)
        :param list_data: list d'objet
        :param title_table: titre du tableau
        :param fields: champs des colonnes à afficher
        :return:
        """
        table = Table(title=title_table)
        for field in fields:
            table.add_column(field.capitalize())
        for data in list_data:
            data_dict = data.to_dict()
            row = [str(data_dict.get(field, "")) for field in fields]
            table.add_row(*row)

        console = Console()
        console.print(table)

    def display_selected_data(self, list_data):
        choices = [
            questionary.Choice(
                title=f"{data}",
                value=data
            )
            for data in list_data
        ]

        data_selected = questionary.select(
            "Sélectionner l'élément (filtrable):",
            choices=choices,
            use_search_filter=True,
            use_jk_keys=False
        ).ask()

        return data_selected

    def display_checkbox_data(self, list_data):
        choices = [
            questionary.Choice(
                title=f"{data}",
                value=data
            )
            for data in list_data
        ]

        data_selected = questionary.checkbox(
            "Sélectionner élément(s) (filtrable):",
            choices=choices,
            use_search_filter=True,
            use_jk_keys=False
        ).ask()

        return data_selected

    def display_modify_data(self,data, fields, technic_fields):
        mapping = dict(zip(fields, technic_fields))
        fields_changed = questionary.checkbox(
            "Quels champs souhaitez-vous modifier ?",
            choices=fields
        ).ask()

        modifications = {}
        for field in fields_changed:
            key_technic = mapping[field]  # récupère la clé technique correspondante
            valeur_actuelle = getattr(data, key_technic, "")
            while True:
                new_value = questionary.text(
                    f"Nouvelle valeur pour {field} (actuel: {valeur_actuelle}) : (laisser vide pour annuler)",
                    validate=lambda text: validate_field(key_technic, text)
                ).ask()

                if new_value:
                    modifications[key_technic] = new_value
                    break
        return modifications