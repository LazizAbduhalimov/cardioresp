from django.apps import AppConfig


class AuthorsProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'
    verbose_name = "Профиль авторов"

    def ready(self):
        import profiles.signals
