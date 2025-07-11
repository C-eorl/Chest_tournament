from datetime import datetime, date

from models.player import Player



class Tournament:

    def __init__(self, tournament_name: str, locality: str, description: str, start_date: date, end_date: date, round_number: int =4):
        self.tournament_name = tournament_name
        self.locality = locality
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.description = description
        self.list_participant = []
        self.statut = "ready"

    def __str__(self):
        start_str = self.start_date.strftime("%d/%m/%Y")
        end_str = self.end_date.strftime("%d/%m/%Y") if self.end_date else "Non défini"
        return f"Tournoi {self.tournament_name} à {self.locality} (Début: {start_str} - Fin: {end_str})"

    def to_dict(self):
        return {
            "tournament_name": self.tournament_name,
            "locality": self.locality,
            "start_date": self.start_date.strftime("%d/%m/%Y"),
            "end_date": self.end_date.strftime("%d/%m/%Y"),
            "round_number": self.round_number,
            "description": self.description,
            "list_participant": [participant.to_dict() for participant in self.list_participant],
            "statut": self.statut
        }

    @classmethod
    def from_dict(cls, data):
        tournament = cls(
            tournament_name = data["tournament_name"],
            locality = data["locality"],
            description = data["description"],
            start_date=datetime.strptime(data["start_date"], "%d/%m/%Y").date(),
            end_date=datetime.strptime(data["end_date"], "%d/%m/%Y").date(),
            round_number = data.get("round_number", 4)
        )
        list_participant = data.get("list_participant", [])
        [Player.from_dict(player) for player in list_participant]
        tournament.statut = data.get("statut", False)
        return tournament

    def ajout_participant(self, joueur: Player):
        """ Ajoute un Joueur au tournoi """
        self.list_participant.append(joueur)


if __name__ == "__main__":
    pass
