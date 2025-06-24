class Tournoi:
    def __init__(self, nom: str, lieu: str, date_debut, date_fin, description: str, nombre_tours: int =4):
        self.nom = nom
        self.lieu = lieu
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nombre_tours = nombre_tours
        self.description = description

    def information_tournoi(self):
        print(f"information: {self.nom}")

