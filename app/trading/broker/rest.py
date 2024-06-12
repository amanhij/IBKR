import json
import os
from json import JSONDecodeError

import requests

from core.models import Order
from trading.core import next_order_number

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
    print(f'REST :: Init :: {response.status_code} {response.text}')


def reauthenticate_gateway():
    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/reauthenticate',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        })
    print(f'REST :: Reauthenticate :: {response} {response.text}')


def get_orders(account_id: str):
    response = requests.get(
        url=f'{IBKR_GATEWAY_URL}/iserver/account/orders?force=false&accountId={account_id}',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        })
    print(f'REST :: Get Orders :: {response.status_code} {response.text}')
    try:
        return response.json()
    except json.decoder.JSONDecodeError:
        return None


def create_bracket_order(account_id: str, con_id: int,
                         action: str, quantity: float,
                         limit_price: float, take_profit_limit_price: float, stop_loss_price: float):
    order_id = next_order_number()
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
                'cOID': next_order_number(),
                'parentId': order_id,
                'conid': con_id,
                'side': 'SELL' if action == 'BUY' else 'BUY',
                'quantity': quantity,
                'orderType': 'LMT',
                'price': take_profit_limit_price,
                'tif': 'GTC',
                'isSingleGroup': True,
                'outsideRTH': False
            },
            {
                'acctId': account_id,
                'cOID': next_order_number(),
                'parentId': order_id,
                'conid': con_id,
                'side': 'SELL' if action == 'BUY' else 'BUY',
                'quantity': quantity,
                'orderType': 'STP',
                'price': stop_loss_price,
                'tif': 'GTC',
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
    print(f'REST :: Create order :: \n\t {payload} \n\t {response.status_code} {response.text}')
    try:
        if response.status_code != 200:
            print(f'REST :: ERROR :: There was an error creating orders :: {payload} :: {response.status_code} {response.text}')
            return None
        return response.json()
    except JSONDecodeError:
        return None


def modify_order(order: Order, price: float):
    payload = {
        'conid': int(order.con_id),
        'side': order.side,
        'quantity': order.total_size,
        'orderType': 'LMT' if order.order_type == 'LIMIT' else 'STP',
        'price': price,
        'tif': 'GTC',
    }

    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/account/{order.account_id}/order/{order.order_id}',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        },
        json=payload)
    print(f'REST :: Updated order :: \n\t {payload} \n\t {response.status_code} {response.text}')
    if response.status_code != 200:
        print(f'REST :: ERROR :: There was an error updating orders :: {payload} :: {response.status_code} {response.text}')


def confirm_message(id: str):
    response = requests.post(
        url=f'{IBKR_GATEWAY_URL}/iserver/reply/{id}',
        headers={
            'Content-Type': 'application/json; charset=UTF-8',
            'Accept': 'application/json; charset=UTF-8'
        },
        json={'confirmed': True})
    if response.status_code != 200:
        print(f'REST :: ERROR :: There was an error confirming messages :: {id} :: {response.status_code} {response.text}')
    else:
        print(f'REST :: Confirm Message :: {response.status_code} {response.text}')
