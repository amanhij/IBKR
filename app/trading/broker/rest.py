import json
import os

import requests

IBKR_GATEWAY_URL = os.getenv('IBKR_GATEWAY_URL')


def init_gateway():
    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/auth/ssodh/init',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        },
        json={
            'publish': True,
            'compete': True
        })
    print(f'REST :: Init :: {response}')


def reauthenticate_gateway():
    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/reauthenticate',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        })
    print(f'REST :: Reauthenticate :: {response}')


def get_orders(account_id: str):
    response = requests.get(
        url=f'{IBKR_GATEWAY_URL}/iserver/account/orders?force=false&accountId={account_id}',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        })
    print(f'REST :: Orders :: {response}')
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        return None


def create_bracket_order(account_id: str, order_id: int, con_id: int, action: str, quantity: float,
                         limit_price: float, take_profit_limit_price: float, stop_loss_price: float):
    payload = {
        'orders': [
            {
                'acctId': account_id,
                'cOID': order_id,
                'conid': con_id,
                'side': action,
                'quantity': quantity,
                'orderType': 'LMT',
                'price': limit_price,
                'tif': 'IOC',
                'isSingleGroup': True,
                'outsideRTH': False
            },
            {
                'acctId': account_id,
                'parentId': order_id,
                'conid': con_id,
                'side': 'SELL' if action == 'BUY' else 'BUY',
                'quantity': quantity,
                'orderType': 'LMT',
                'price': take_profit_limit_price,
                'tif': 'IOC',
                'isSingleGroup': True,
                'outsideRTH': False
            },
            {
                'acctId': account_id,
                'parentId': order_id,
                'conid': con_id,
                'side': 'SELL' if action == 'BUY' else 'BUY',
                'quantity': quantity,
                'orderType': 'STP',
                'price': stop_loss_price,
                'tif': 'IOC',
                'isSingleGroup': True,
                'outsideRTH': False
            }
        ]}
    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/account/{account_id}/orders/whatif',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        },
        json=payload)
    print(f'REST :: Create order :: {response}')
