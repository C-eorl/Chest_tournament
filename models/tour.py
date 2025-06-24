from match import Match

class Tour:
    def __init__(self, list_match: list[Match], nom: str, date_heure_debut, date_heure_fin):
        self.list_match = list_match
        self.nom = nom
        self.date_heure_debut = date_heure_debut
        self.date_heure_fin = date_heure_fin

    # fonction auto date/heure debut tours
    # fonction auto date/heure fin tours
