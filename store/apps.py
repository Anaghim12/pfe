from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    # this is to import the code of the signal 
    def ready(self) -> None:
        import store.signals.handlers