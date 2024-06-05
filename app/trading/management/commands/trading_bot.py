import time

from django.core.management import BaseCommand

from trading.broker import run_websocket
from trading.core import sync_orders_async


class Command(BaseCommand):

    def handle(self, *args, **options):
        while True:
            # sync orders
            sync_orders_async()
            # start websocket
            run_websocket()

