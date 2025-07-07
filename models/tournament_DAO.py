from tinydb import Query


class TournamentRepository:
    def __init__(self, db):
        self.db = db
        self.TournamentQuery = Query()

    def add_db(self, data):
        self.db.insert(dict(data))

    def tournament_exist(self, name: str) -> bool:
        return self.db.search(self.TournamentQuery.name == name)