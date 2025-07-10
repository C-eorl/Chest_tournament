def retour():
    """Appel interne de la fonction pour affiche le menu principal"""
    from controllers.controller_interface import ControllerInterface
    controller = ControllerInterface()
    return controller.run()