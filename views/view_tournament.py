import questionary
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

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
        name = (questionary.text(
            "Nom du tournoi",
            validate=lambda text: validate_field("tournament_name", text)
            ).ask())
        locality = (questionary.text(
            "Ville: ",
            validate=lambda text: validate_field("locality", text)
            ).ask())
        round_number = (questionary.text(
            "Nombre de round: ",
            default="4",
            validate=lambda text: validate_field("round_number", text)
            ).ask())
        description = questionary.text(
            "Description: ",
            validate=lambda text: validate_field("description", text)
            ).ask()
        start_date = questionary.text(
            "Date de début du tournoi: ",
            validate=lambda text: validate_field("start_date", text)
            ).ask()
        end_date = questionary.text(
            "Date de fin du tournoi: ",
            validate=lambda text: validate_field("end_date", text)
            ).ask()

        return [name, locality, description, start_date, end_date, round_number]

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
        """Affiche les informations d'un tournoi"""
        table = Table(show_header=False, header_style="bold magenta")
        table.add_column("Champ")
        table.add_column("Valeur", style="bold cyan", width=25)

        table.add_row("Nom", tournament.tournament_name)
        table.add_row("Lieu", tournament.locality)
        table.add_row("Date de début", tournament.start_date.strftime("%d/%m/%Y"))
        table.add_row("Date de fin", tournament.end_date.strftime("%d/%m/%Y"))
        table.add_row("Nombre de round", str(tournament.round_number))
        table.add_row("Description", tournament.description)
        table.add_row("Statut", tournament.statut, style="red")

        panel = Panel(
            table,
            title=f"[bold #29a7ab]Tournoi : {tournament.tournament_name}",
            border_style="#29a7ab",
            expand=False,

        )
        self.console.print(panel)
        sorted_classement = dict(sorted(tournament.classement.items(), key=lambda x: x[1], reverse=True))
        self.display_classement(sorted_classement)

    def display_round(self, round):
        """Affiche les informations d'un Round"""
        console = Console()

        title = Text(f"🏆 {round.name}", style="bold #29a7ab", justify="center")
        console.print(Panel(title, style="#29a7ab", padding=(1, 2)))

        table = Table(title="📋 Liste des Matchs",
                      box=box.ROUNDED,
                      show_header=True,
                      expand=True)
        table.add_column("Joueur 1", style="#29a7ab", width=20)
        table.add_column("Score", justify="center", style="#ed7f07 bold", width=10)
        table.add_column("Joueur 2", style="#29a7ab", width=20)

        list_match = round.get_match_list()
        lone_player = round.lone_player
        for match in list_match:
            score_text = f"{match.score1} - {match.score2}"
            table.add_row(match.player1.simple_str(), score_text, match.player2.simple_str())
            table.add_row("", "", "")
        if lone_player:
            table.add_row(lone_player.simple_str(), "1.0 - 0.0", " / ")
        console.print(table)

    def confirmed_message(self):
        self.display_message("Le tournoi choisi est en cours."
                             "\nL'ajout de nouveau participant peut avoir des résultats non attendu")
        choices = ["oui", "non"]
        anwers = questionary.select(
            "Êtes-vous sure de continuer ?",
            choices=choices,
            qmark="✦",
            instruction="\n[↑] & [↓] pour naviguer, [Entrée] pour valider"
        ).ask()
        if anwers == "oui":
            return True
        else:
            return False

    def display_classement(self, classement):
        """Affiche le classement d'un tournoi
        :param classement : dict {Player: score}
        """
        console = Console()
        table = Table(
            title="\n[#29a7ab bold]Classement",
        )
        table.add_column("Joueur")
        table.add_column("Score", style="#29a7ab")
        for player, score in classement.items():
            table.add_row(player.simple_str(), str(score))
        console.print(table)
