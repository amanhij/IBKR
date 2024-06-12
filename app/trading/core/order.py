import threading
from datetime import datetime, timezone

from core.models import Order, Strategy, Price, OrderSide


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
    from trading.broker import create_bracket_order
    delta = 10 ** -strategy.precision
    response = create_bracket_order(
        strategy.account_id,
        int(strategy.contract.con_id),
        strategy.side,
        strategy.quantity,
        round(current_price.ask + delta if strategy.side == OrderSide.BUY else current_price.bid - delta, strategy.precision),
        round(current_price.last * strategy.limit_factor, strategy.precision),
        round(current_price.last * strategy.stop_factor, strategy.precision),
    )
    if response is not None:
        for order in response:
            if 'id' in order:
                from trading.broker import confirm_message
                confirm_message(order['id'])


def update_windows(strategy: Strategy, current_price: Price):
    from trading.broker import modify_order
    side_filter = OrderSide.BUY if strategy.side == OrderSide.SELL else OrderSide.SELL
    stop_limit_orders = Order.objects.filter(
        parent_id__isnull=False,
        account_id=strategy.account_id,
        con_id=strategy.contract.con_id,
        side=side_filter,
        status__in=['Submitted', 'PreSubmitted'])
    for order in stop_limit_orders:
        modify_order(
            order,
            round(current_price.last *
                  (strategy.limit_factor if order.order_type == 'LIMIT' else strategy.stop_factor), strategy.precision),
        )


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
