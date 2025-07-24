import questionary
from utils.validation import validate_field
from views.view import View


class ViewPlayer(View):

    def input_player(self):

        firstname = questionary.text("Prénom :",
                                     validate=lambda text: validate_field("firstname", text),
                                     qmark="✦",
                                     ).ask()
        if firstname:
            firstname = firstname.capitalize()
        name = questionary.text("Nom :",
                                validate=lambda text: validate_field("name", text),
                                qmark="✦",
                                ).ask()
        if name:
            name = name.capitalize()
        birthdate = questionary.text(
            "Date de naissance (dd/mm/aaaa) :",
            validate=lambda text: validate_field("birthdate",text),
            qmark="✦",
        ).ask()
        id_chess = questionary.text("ID national d'échec (ex: AA12345) :",
                                    validate=lambda text: validate_field("id_chess", text),
                                    qmark="✦",
                                    ).ask()

        return [name, firstname, birthdate, id_chess]