from functools import wraps


def decorator_try(fonction):
    @wraps(fonction)
    def wrapper(*args):
        try:
            return fonction(*args)
        except TypeError as e:
            print(f"[ERREUR] fonction:{fonction.__name__} - {e}")
        except KeyError:
            print("Annulation via Ctrl+c")
    return wrapper
