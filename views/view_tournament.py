from datetime import datetime

import questionary
from utils.validation import validate_field
from views.view import View


class ViewTournament(View):

    def input_tournament(self):
        """
        Demande à l'utilisateur les information pour le nouveau tournoi
        :return: dict des valeurs pour objet Tournament
        """
        name = questionary.text("Nom du tournoi", validate=lambda text: validate_field("tournament_name", text)).ask()
        locality = questionary.text("Ville: ", validate=lambda text: validate_field("locality", text)).ask()
        round_number = questionary.text("Nombre de round: ", default="4", validate=lambda text: validate_field("round_number", text)).ask()
        description = questionary.text("Description: ", validate=lambda text: validate_field("description", text)).ask()
        start_date = questionary.text("Date de début du tournoi: ", validate=lambda text: validate_field("start_date", text)).ask()
        end_date = questionary.text("Date de fin du tournoi: ", validate=lambda text: validate_field("end_date", text)).ask()

        start_date = datetime.strptime(start_date, "%d/%m/%Y").date()
        end_date = datetime.strptime(end_date, "%d/%m/%Y").date()

        return [name, locality, description, start_date, end_date, int(round_number)]

    def display_tournament(self, list_current_tournament):
        """
        affiche la liste des tournois en cours avec selection unique
        :param list_current_tournament: list d'objet Tournament avec le statut "current"
        :return: Tournament sélectionné
        """
        choices = [
            questionary.Choice(
                title=f"{current_tournament}",
                value=current_tournament
            )
            for current_tournament in list_current_tournament
        ]
        target = questionary.select(
            "Quel tournoi voulez-vous sélectionner ?",
            choices=choices).ask()
        return target