from datetime import datetime


class Round:

    def __init__(self, name: str):
        self.list_match = []
        self.name = name
        self.date_time_start = None
        self.date_time_end = None

    def __str__(self):
        return f"{self.name} avec comme resultat : {self.list_match}"

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