from datetime import datetime

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from models.tournament import Tournament
from utils.validation import validate_field
from views.view import View


class ViewTournament(View):
    def __init__(self):
        self.console = Console()
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

    def display_selected_tournament(self, list_current_tournament) -> Tournament:
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

    def display_tournament(self, tournament):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Champ")
        table.add_column("Valeur", style="bold cyan")

        table.add_row("Nom", tournament.tournament_name)
        table.add_row("Lieu", tournament.locality)
        table.add_row("Date de début", tournament.start_date.strftime("%d/%m/%Y"))
        table.add_row("Date de fin", tournament.end_date.strftime("%d/%m/%Y"))
        table.add_row("Nombre de round", str(tournament.round_number))
        table.add_row("Description", tournament.description)
        table.add_row("Statut", tournament.statut, style="red")

        table_participant = Table(show_header=True)
        table_participant.add_column("Participant")
        table_participant.add_column("Score")
        for participant in tournament.list_participant:
            table_participant.add_row( str(participant), "score")



        panel = Panel(table, title=f"[bold green]Tournoi : {tournament.tournament_name}", border_style="green")
        panel_participant = Panel(table_participant)
        self.console.print(panel)
        self.console.print(panel_participant)
