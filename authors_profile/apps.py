from django.apps import AppConfig


class AuthorsProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authors_profile'
    verbose_name = "Профиль авторов"

    def ready(self):
        import authors_profile.signals
