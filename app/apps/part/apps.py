from django.apps import AppConfig


class PartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.part"

    def ready(self):
        import part.signals  # noqa: F401
