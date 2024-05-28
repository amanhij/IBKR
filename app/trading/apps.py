from django.apps import AppConfig

from .broker.websocket import start_connection


class CoreConfig(AppConfig):
    name = 'trading'

    def ready(self):
        start_connection()
