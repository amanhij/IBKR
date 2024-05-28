import json
import os
import ssl
import threading
import time
from datetime import datetime, timezone

import websocket


class WebSocketClient:
    def __init__(self, uri):
        self.prev_time = time.gmtime()
        self.prev_price = None
        self.ws = websocket.WebSocketApp(
            url=uri,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

    def on_message(self, ws, message):
        print(f'WS :: Message :: {message}')
        payload = json.loads(message.decode("utf-8"))
        if payload['topic'].startswith('smd+') and "31" in payload:
            current_time = time.gmtime(payload['_updated'] / 1000)
            if current_time.tm_min != self.prev_time.tm_min:
                contid = payload['topic'][4:]
                data = dict(
                    last=payload["31"],
                    bid=payload["84"] if "84" in payload else None,
                    ask=payload["86"] if "86" in payload else None
                )
                from core.models import Price
                update_time = datetime.fromtimestamp(payload['_updated'] / 1000, tz=timezone.utc)
                Price.objects.update_or_create(conid=contid, update_time=update_time, defaults=data)
                print(f'WS :: {contid} :: {time.strftime("%Y-%m-%d %H:%M:%SZ", current_time)}, Last: {payload["31"]}')
                self.prev_time = current_time

    def on_error(self, ws, error):
        print(f'WS :: Error :: {error}')

    def on_close(self, ws, message, detail):
        print(f'WS :: Closed :: {message} :: {detail}')

    def on_open(self, ws):
        print('WS :: Connection Opened')
        time.sleep(3)
        from core.models import Contract
        for contract in Contract.objects.all():
            print(f'WS :: Subscribing to contract {contract.conid}')
            ws.send('smd+' + contract.conid + '+{"fields": ["31", "83", "84", "85", "86"]}')
        print(f'WS :: init done!')

    def run(self):
        self.ws.run_forever(sslopt={'cert_reqs': ssl.CERT_NONE})


def start_connection():
    uri = os.getenv('IBKR_GATEWAY_WS')
    if uri:
        client = WebSocketClient(uri)
        ws_thread = threading.Thread(target=client.run, daemon=True)
        ws_thread.start()
