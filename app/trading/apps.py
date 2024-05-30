from django.apps import AppConfig

from .broker.websocket import start_websocket
from .strategy import sync_strategy


class CoreConfig(AppConfig):
    name = 'trading'

    def ready(self):
        # start websocket
        start_websocket()
        # sync strategy
        sync_strategy()
