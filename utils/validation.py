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

        case "birthdate":
            pattern_date = r"^([0-2][0-9]|3[01])/([0][1-9]|1[0-2])/(\d{4})$"
            if not re.match(pattern_date, value):
                return "Format invalide (dd/mm/aaaa)"
            return True

        case "id_chess":
            pattern_id = r'^[A-Z]{2}\d{5}$'
            if not re.match(pattern_id, value):
                return "Format invalide (ex: AA12345)"
            return True

        case _:
            return f"Champ inconnu : {field_name}"
