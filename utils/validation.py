import re

def validate_field(field_name: str, value: str) -> bool | str:
    """
    Valide la valeur selon le champ (field_name).
    Retourne True si valide, sinon un message d'erreur.
    """

    match field_name:
        case "firstname" | "name":
            if not value or any(char.isdigit() for char in value):
                return f"Le {field_name} ne doit pas contenir de chiffres et ne peut pas être vide"
            return True

        case "birthdate" | "end_date" | "start_date":
            pattern_date = r"^([0-2][0-9]|3[01])/([0][1-9]|1[0-2])/(\d{4})$"
            if not re.match(pattern_date, value):
                return "Format invalide (dd/mm/aaaa)"
            return True

        case "id_chess":
            pattern_id = r'^[A-Z]{2}\d{5}$'
            if not re.match(pattern_id, value):
                return "Format invalide (ex: AA12345)"
            return True

        case "tournament_name":
            if not value.strip():
                return "Le nom du tournoi ne peut pas être vide"
            return True

        case "locality":
            if not value.strip() or any(char.isdigit() for char in value):
                return "La localité ne peut pas être vide ni contenir de chiffres"
            return True

        case "round_number":
            if not value.isdigit():
                return "Le nombre de rounds doit être un entier positif"
            return True

        case "description":
            if not value.strip():
                return "La description ne peut pas être vide"
            return True

        case "statut":
            if value not in ["ready", "current", "finished"]:
                return "Le statut ne peut être que: ready, current, finished"
            return True

        case _:
            return f"Champ inconnu : {field_name}"
