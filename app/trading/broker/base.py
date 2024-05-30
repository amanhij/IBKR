import time
from datetime import datetime, timezone
from typing import List


class ProcessMessage:
    def __init__(self):
        self.prev_time = time.gmtime()
        self.prev_last_price = None
        self.prev_bid_price = None
        self.prev_ask_price = None

    def request_market_data_message(self, conid: str) -> str:
        return 'smd+' + conid + '+{"fields": ["31", "83", "84", "85", "86"]}'

    def is_market_data_message(self, payload: dict) -> bool:
        return 'topic' in payload and payload['topic'].startswith('smd+')

    def process_market_data_message(self, payload: dict):
        current_time = time.gmtime(payload['_updated'] / 1000)
        if '31' in payload and current_time.tm_min != self.prev_time.tm_min:
            con_id = payload['topic'][4:]
            data = dict(
                last=payload['31'],
                bid=payload['84'] if '84' in payload else self.prev_bid_price,
                ask=payload['86'] if '86' in payload else self.prev_ask_price)
            from core.models import Price
            update_time = datetime.fromtimestamp(payload['_updated'] / 1000, tz=timezone.utc)
            Price.objects.update_or_create(con_id=con_id, update_time=update_time, defaults=data)
            self.prev_time = current_time
        self.prev_bid_price = payload['84'] if '84' in payload else self.prev_bid_price
        self.prev_ask_price = payload['86'] if '86' in payload else self.prev_ask_price

    def request_order_operations_message(self) -> str:
        return 'sor+{}'

    def is_order_operations_message(self, payload: dict) -> bool:
        return 'topic' in payload and payload['topic'].startswith('sor+')

    def process_order_operations_message(self, payload: dict):
        pass

    def request_profit_and_lost_message(self) -> str:
        return 'spl+{}'

    def is_profit_and_lost_message(self, payload: dict) -> bool:
        return 'topic' in payload and payload['topic'].startswith('spl+')

    def process_profit_and_lost_message(self, payload: dict):
        pass

    def is_system_message(self, payload: dict) -> bool:
        return 'topic' in payload and payload['topic'].startswith('system')

    def process_system_message(self, payload: dict):
        pass
