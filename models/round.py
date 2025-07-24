from datetime import datetime

from models.match import Match
from models.player import Player


class Round:

    def __init__(self, name: str):
        self.list_match = []
        self.name = name
        self.date_time_start = None
        self.date_time_end = None
        self.lone_player = None

    def __str__(self):
        return f"{self.name} avec comme resultat : {self.list_match}"

    def to_dict(self):
        return {
            "name": self.name,
            "list_match": [match.to_dict() for match in self.list_match],
            "lone_player": self.lone_player.to_dict() if self.lone_player else None,
            "start_date": self.date_time_start.strftime("%d/%m/%Y %H:%M:%S") if self.date_time_start else None,
            "end_date": self.date_time_end.strftime("%d/%m/%Y %H:%M:%S") if self.date_time_end else None
        }

    @classmethod
    def from_dict(cls, data):
        round = cls(data["name"])
        round.list_match = [Match.from_dict(m) for m in data.get("list_match", [])]
        lone_player = data.get("lone_player")
        round.lone_player = Player.from_dict(lone_player) if lone_player else None
        if data.get("start_date"):
            round.date_time_start = datetime.strptime(data["start_date"], "%d/%m/%Y %H:%M:%S")
        if data.get("end_date"):
            round.date_time_end = datetime.strptime(data["end_date"], "%d/%m/%Y %H:%M:%S")
        return round

    def start(self):
        """défini le debut du round"""
        self.date_time_start = datetime.now()

    def finish(self):
        self.date_time_end = datetime.now()

    def get_match_list(self):
        """retourne la liste des matchs"""
        return self.list_match

if __name__ == "__main__":
    pass