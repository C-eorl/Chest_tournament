import questionary

from rich.table import Table
from rich.console import Console


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