from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # включва търсенето с малки/главни букви на кирилица (виж TroyaMig/sqlite_unicode.py)
        from TroyaMig import sqlite_unicode  # noqa: F401
