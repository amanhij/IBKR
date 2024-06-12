import threading
import time
from datetime import datetime, timezone

from core.models import Order, Strategy, Price, OrderSide
from trading.core import next_order_number


def sync_orders():
    from core.models import Strategy
    account_ids = Strategy.objects.order_by().values_list('account_id', flat=True).distinct()
    for account_id in account_ids:
        from trading.broker import get_orders
        orders = get_orders(account_id)
        if orders is None or not 'orders' in orders:
            continue
        for order in orders['orders']:
            update_order(order)


def create_order(strategy: Strategy, current_price: Price):
    delta = 10 ** -strategy.precision
    parent_id = next_order_number()
    now = int(time.time()) * 1000
    update_order({
        'account': strategy.account_id,
        'conid': int(strategy.contract.con_id),
        'orderId': parent_id,
        'order_ref': parent_id,
        'lastExecutionTime_r': now,
        'side': strategy.side,
        'origOrderType': 'LIMIT',
        'status': 'Filled',
        'order_ccp_status': 'Filled',
        'totalSize': '1',
        'price': round(current_price.ask + delta if strategy.side == OrderSide.BUY else current_price.bid - delta, strategy.precision),
    })

    order_id = next_order_number()
    update_order({
        'account': strategy.account_id,
        'conid': int(strategy.contract.con_id),
        'parentId': parent_id,
        'orderId': order_id,
        'order_ref': order_id,
        'lastExecutionTime_r': now,
        'side': 'SELL' if strategy.side == 'BUY' else 'BUY',
        'origOrderType': 'LIMIT',
        'status': 'Submitted',
        'order_ccp_status': 'Replaced',
        'totalSize': '1',
        'price': round(current_price.last * strategy.limit_factor, strategy.precision)
    })

    order_id = next_order_number()
    update_order({
        'account': strategy.account_id,
        'conid': int(strategy.contract.con_id),
        'parentId': parent_id,
        'orderId': order_id,
        'order_ref': order_id,
        'lastExecutionTime_r': now,
        'side': 'SELL' if strategy.side == 'BUY' else 'BUY',
        'origOrderType': 'STOP',
        'status': 'PreSubmitted',
        'order_ccp_status': 'Replaced',
        'totalSize': '1',
        'stop_price': round(current_price.last * strategy.stop_factor, strategy.precision)
    })


def update_windows(strategy: Strategy, current_price: Price):
    # from trading.broker import modify_order
    side_filter = OrderSide.BUY if strategy.side == OrderSide.SELL else OrderSide.SELL
    stop_limit_orders = Order.objects.filter(
        parent_id__isnull=False,
        account_id=strategy.account_id,
        con_id=strategy.contract.con_id,
        side=side_filter,
        status__in=['Submitted', 'PreSubmitted'])
    for order in stop_limit_orders:
        if order.order_type == 'STOP':
            update_order({
                'orderId': order.order_id,
                'stop_price': round(current_price.last, strategy.precision)
            })
        else:
            update_order({
                'orderId': order.order_id,
                'price': round(current_price.last * strategy.limit_factor, strategy.precision)
            })


def auto_close(strategy: Strategy, current_price: Price):
    side_filter = OrderSide.BUY if strategy.side == OrderSide.SELL else OrderSide.SELL
    stop_limit_orders = Order.objects.filter(
        parent_id__isnull=False,
        side=side_filter,
        status__in=['Submitted', 'PreSubmitted'])
    now = int(time.time()) * 1000
    for order in stop_limit_orders:
        if ((order.side == 'SELL' and order.order_type == 'STOP' and order.stop_price > current_price.last)
                or (order.side == 'BUY' and order.order_type == 'STOP' and order.stop_price < current_price.last)):
            update_order({
                'orderId': order.order_id,
                'status': 'Filled',
                'lastExecutionTime_r': now
            })
            limit_order = Order.objects.filter(parent_id=order.parent_id, order_type='LIMIT').first()
            update_order({
                'orderId': limit_order.order_id,
                'status': 'Cancelled',
                'lastExecutionTime_r': now
            })
        elif ((order.side == 'SELL' and order.order_type == 'LIMIT' and order.price < current_price.last)
              or (order.side == 'BUY' and order.order_type == 'LIMIT' and order.price > current_price.last)):
            update_order({
                'orderId': order.order_id,
                'status': 'Filled',
                'lastExecutionTime_r': now
            })
            stop_order = Order.objects.filter(parent_id=order.parent_id, order_type='STOP').first()
            update_order({
                'orderId': stop_order.order_id,
                'status': 'Cancelled',
                'lastExecutionTime_r': now
            })


def update_order(order: dict):
    try:
        data = {}
        if 'account' in order:
            data['account_id'] = order['account']
        if 'conid' in order:
            data['con_id'] = order['conid']
        if 'parentId' in order:
            data['parent_id'] = order['parentId']
        if 'orderId' in order:
            data['order_id'] = order['orderId']
        if 'order_ref' in order:
            data['order_ref'] = order['order_ref']
        if 'orderDesc' in order:
            data['order_description'] = order['orderDesc']
        if 'lastExecutionTime_r' in order:
            data['last_execution_time'] = datetime.fromtimestamp(order['lastExecutionTime_r'] / 1000, tz=timezone.utc)
        if 'side' in order:
            data['side'] = order['side']
        if 'origOrderType' in order:
            data['order_type'] = order['origOrderType']
        if 'status' in order:
            data['status'] = order['status']
        if 'order_ccp_status' in order:
            data['ccp_status'] = order['order_ccp_status']
        if 'totalSize' in order:
            data['total_size'] = float(order['totalSize'])
        if 'price' in order:
            data['price'] = float(order['price'])
        if 'avgPrice' in order:
            data['avg_price'] = float(order['avgPrice'])
        if 'stop_price' in order:
            data['stop_price'] = float(order['stop_price'])
        Order.objects.update_or_create(order_id=order['orderId'], defaults=data)
    except Exception as ex:
        print(f'ORDER :: Exception :: {order} {ex}')


def sync_orders_async():
    thread = threading.Thread(target=sync_orders, daemon=True)
    thread.start()
