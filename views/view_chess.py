import re
from calendar import month
from datetime import date, datetime
from os.path import split

class View:

    def input_joueur(self):
        print("Ajoutez nouveau joueur ")
        while True:

            prenom = input("Prénom : ").capitalize()
            if prenom.isdigit():
                print("Erreur sur le prénom")
                prenom = input("Prénom : ").capitalize()

            nom = input("Nom : ").capitalize()
            if nom.isdigit():
                print("Erreur sur le nom")
                nom = input("nom : ").capitalize()

            date_naissance = input("Date de naissance (dd/mm/aaaa) : ")
            pattern_date = r"^([0-2][0-9]|3[01])/([0][1-9]|1[0-2])/(\d{4})$"
            if not re.match(pattern_date, date_naissance):
                print("Erreur date de naissance")
                date_naissance = input("Date de naissance (dd/mm/aaaa) : ")

            id_echec = input("ID nationnal d'échec (AA12345): ")
            pattern_id = r'^[A-Z]{2}\d{5}$'
            if not re.match(pattern_id, id_echec):
                print("Erreur ID nationnal d'échec (ex: JK45129)")
                id_echec = input("ID nationnal d'échec : ")

            return [prenom, nom, date_naissance, id_echec]


if __name__ == "__main__" :
    pass