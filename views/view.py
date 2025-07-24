import questionary
from rich import print
from rich.table import Table
from rich.console import Console
from utils.validation import validate_field


class View:
    def separator(self):
        print("\n" + "=" * 75 + "\n")

    def menu(self, titre, options):
        """
        Affiche un menu interactif dans le terminal.
        :param titre: Le titre affiché au-dessus des choix.
        :param options: Un dictionnaire où les clés sont les libellés affichés,
                        et les valeurs sont des fonctions à exécuter.
        """
        style = questionary.Style([
            ("question", "bold #a5f2f2"),
            ("answer", "#29a7ab bold"),
            ("instruction", "#a0adad")
        ])
        self.separator()
        choix = questionary.select(
            titre,
            choices=list(options.keys()),
            instruction="   - [↑] & [↓] pour naviguer, [Entrée] pour valider\n",
            qmark="▶",
            style=style
        ).ask()
        if choix is None:
            return None
        return options[choix]

    def display_message(self, message):
        """ Affiche un message
        :param message: str
        """
        print(f"\n[bold]{message}")

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
        :return: None
        """
        table = Table(title=title_table)
        for field in fields:
            table.add_column(
                field.capitalize(),
                width=15,
                header_style="cyan bold"
            )
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
                value=data,
            )
            for data in list_data
        ]
        style = questionary.Style([
            ("question", "bold #a5f2f2"),
            ("instruction", "#a0adad")
        ])
        data_selected = questionary.select(
            "Sélectionner l'élément :",
            style=style,
            choices=choices,
            use_search_filter=True,
            use_jk_keys=False,
            qmark="▶",
            instruction="\nUtilisez [Espace] pour cocher, [↑] & [↓] pour naviguer, [Entrée] pour valider"
                        "\nPossibilité de filtrage textuel\n"
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
        style = questionary.Style([
            ("question", "bold #a5f2f2"),
            ("instruction", "#a0adad")
        ])
        data_selected = questionary.checkbox(
            "Sélectionner élément(s) (filtrable):",
            style=style,
            choices=choices,
            use_search_filter=True,
            use_jk_keys=False,
            qmark="▶",
            instruction="\nUtilisez [Espace] pour cocher, [↑] & [↓] pour naviguer, [Entrée] pour valider",
        ).ask()

        return data_selected

    def display_modify_data(self, data, fields, technic_fields):
        mapping = dict(zip(fields, technic_fields))
        style = questionary.Style([
            ("question", "bold #a5f2f2"),
            ("instruction", "#a0adad")
        ])
        fields_changed = questionary.checkbox(
            "Quels champs souhaitez-vous modifier ?",
            style=style,
            choices=fields,
            qmark="▶",
            instruction="\nUtilisez [Espace] pour cocher, [↑] & [↓] pour naviguer, [Entrée] pour valider"
        ).ask()

        modifications = {}
        if fields_changed:
            for field in fields_changed:
                key_technic = mapping[field]  # récupère la clé technique correspondante
                valeur_actuelle = getattr(data, key_technic, "")
                while True:
                    new_value = questionary.text(
                        f"Nouvelle valeur pour {field} (actuel: {valeur_actuelle}) :",
                        validate=lambda text: validate_field(key_technic, text)
                    ).ask()
                    if new_value is None:
                        self.display_message("Modification annulée")
                        break
                    if new_value:
                        modifications[key_technic] = new_value
                        break
        return modifications
