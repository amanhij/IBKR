import json
import os
import ssl
import time

import websocket

from .base import ProcessMessage
from .rest import init_gateway
from ..strategy import clemence_clementine_run_async


class WebSocketClient:
    def __init__(self, uri):
        self.processMessage = ProcessMessage()
        self.ws = websocket.WebSocketApp(
            url=uri,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

    def on_message(self, ws, message):
        print(f'WS :: Message :: {message}')
        payload = json.loads(message.decode('utf-8'))
        if self.processMessage.is_market_data_message(payload):
            if self.processMessage.process_market_data_message(payload):
                clemence_clementine_run_async()
        elif self.processMessage.is_order_operations_message(payload):
            self.processMessage.process_order_operations_message(payload)
        elif self.processMessage.is_profit_and_lost_message(payload):
            self.processMessage.process_profit_and_lost_message(payload)
        elif self.processMessage.is_system_message(payload):
            self.processMessage.process_system_message(payload)
        elif ('message' in payload and payload['message'] == 'waiting for session') \
                or ('error' in payload and payload['error'] == 'not authenticated'):
            ws.close()

    def on_error(self, ws, error):
        print(f'WS :: Error :: {error}')
        ws.close()

    def on_close(self, ws, message, detail):
        print(f'WS :: Closed :: {message} :: {detail}')

    def on_open(self, ws):
        print('WS :: Connection Opened')
        time.sleep(3)
        self.init(ws)

    def run(self):
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})
        print(f'WS :: Execution Stopped')

    def init(self, ws):
        # subscribe to contracts
        from core.models import Contract
        for contract in Contract.objects.all():
            print(f'WS :: Subscribing to contract {contract.con_id}')
            msg = self.processMessage.request_market_data_message(contract.con_id)
            ws.send(msg)

        # subscribe to account info
        print('WS :: Subscribing to account info')
        msg = self.processMessage.request_order_operations_message()
        ws.send(msg)

        print('WS :: Subscribing to profit and lost info')
        msg = self.processMessage.request_profit_and_lost_message()
        ws.send(msg)

        print(f'WS :: init done!')


def run_websocket():
    uri = os.getenv('IBKR_GATEWAY_WS')
    if uri:
        init_gateway()
        time.sleep(10)
        client = WebSocketClient(uri)
        client.run()
        time.sleep(10)
