import questionary


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
        """ Affiche du texte
        :param message: str
        """
        print(message)

    def display_error(self):
        print("Error")