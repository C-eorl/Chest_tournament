from datetime import datetime, date

from models.player import Player
from models.round import Round


class Tournament:

    def __init__(self, tournament_name: str, locality: str, description: str, start_date: date, end_date: date, round_number: int =4):
        self.tournament_name = tournament_name
        self.locality = locality
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.description = description
        self.statut = "ready"
        self.list_participant = [] # [*Player]
        self.classement = {}  # {Player : score}
        self.rounds = []
        self.match_history = set()


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
            "statut": self.statut,
            "classement": [
                {"player": player.to_dict(), "score": score}
                for player, score in self.classement.items()
            ],
            "rounds": [r.to_dict() for r in self.rounds],
            "match_history": [
                (p1.name, p2.name) for (p1, p2) in self.match_history
            ]
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
        tournament.list_participant = [Player.from_dict(player) for player in list_participant]
        tournament.statut = data.get("statut", "ready")
        tournament.classement = {
            Player.from_dict(item["player"]): item["score"]
            for item in data.get("classement", [])
        }
        tournament.rounds = [
            Round.from_dict(r) for r in data.get("rounds", [])
        ]
        name_to_player = {p.name: p for p in tournament.list_participant}
        tournament.match_history = {
            tuple(sorted(
                [name_to_player[n1], name_to_player[n2]],
                key=lambda p: p.name
            ))
            for n1, n2 in data.get("match_history", [])
            if n1 in name_to_player and n2 in name_to_player
        }
        return tournament

    def ajout_participant(self, joueur: Player):
        """ Ajoute un Joueur au tournoi """
        self.list_participant.append(joueur)


if __name__ == "__main__":
    pass
