from django.apps import AppConfig

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MAIN'

    def ready(self):
        import MAIN.signals  # Import sygnałów
