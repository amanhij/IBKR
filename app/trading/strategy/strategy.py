import threading
import time
from datetime import datetime, timezone

from trading.broker.rest import get_orders


def sync_orders():
    from core.models import Strategy
    account_ids = Strategy.objects.order_by().values_list('account_id', flat=True).distinct()
    for account_id in account_ids:
        orders = get_orders(account_id)
        if orders is None or not 'orders' in orders:
            continue
        for order in orders['orders']:
            last_execution_time = datetime.fromtimestamp(order['lastExecutionTime_r'] / 1000, tz=timezone.utc)
            data = dict(
                account_id=order['account'],
                con_id=order['conid'],
                parent_id=order['parentId'] if 'parentId' in order else None,
                order_id=order['orderId'],
                order_ref=order['order_ref'] if 'order_ref' in order else None,
                order_description=order['orderDesc'],
                last_execution_time=last_execution_time,
                side=order['side'],
                order_type=order['origOrderType'],
                status=order['status'],
                total_size=float(order['totalSize']),
                price=float(order['price']) if 'price' in order else None,
                avg_price=float(order['avgPrice']) if 'avgPrice' in order else None,
                stop_price=float(order['stop_price']) if 'stop_price' in order else None
            )
            from core.models import Order
            Order.objects.update_or_create(order_id=order['orderId'], defaults=data)


def _wait_and_sync_orders():
    time.sleep(10)
    sync_orders()


def sync_strategy():
    ws_thread = threading.Thread(target=_wait_and_sync_orders, daemon=True)
    ws_thread.start()
