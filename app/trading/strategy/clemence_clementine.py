import threading

from core.models import Price, OrderSide, Strategy
from trading.core import create_order, update_windows


def clemence_clementine_run_async():
    thread = threading.Thread(target=clemence_clementine_run, daemon=True)
    thread.start()


def clemence_clementine_run():
    strategies = Strategy.objects.all()
    for strategy in strategies:
        current_price, last_price = get_prices(strategy.contract.con_id)
        if ((strategy.side == OrderSide.BUY and current_price.last > last_price.last)
                or (strategy.side == OrderSide.SELL and current_price.last < last_price.last)):
            create_order(strategy, current_price)
            update_windows(strategy, current_price)


def get_prices(con_id: str) -> (Price, Price):
    prices = Price.objects.filter(con_id=con_id).order_by('-update_time')[:2]
    if len(prices) < 2:
        pass
    return prices[0], prices[1]
