from django.apps import AppConfig


class VebetappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vebetapp'

    def ready(self):
        import vebetapp.signals