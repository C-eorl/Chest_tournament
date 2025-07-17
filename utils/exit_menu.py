def retour():
    """Appel interne de la fonction pour affiche le menu principal"""
    from controllers.app_controller import AppController
    controller = AppController()
    return controller.run()