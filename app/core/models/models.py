from django.db import models

from .models_types import OrderSide


class Contract(models.Model):
    con_id = models.CharField('Contract Id', max_length=16, blank=False, null=False)
    name = models.CharField(max_length=32, blank=False, null=False)

    class Meta:
        unique_together = ['con_id', 'name']
        verbose_name_plural = 'Contracts'

    def __str__(self):
        return f'{self.name} :: {self.con_id}'


class Strategy(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=False)
    side = models.CharField(max_length=4, choices=OrderSide.choices, default=OrderSide.BUY, blank=False, null=False)
    account_id = models.CharField(max_length=16, blank=False, null=False)
    quantity = models.FloatField(null=False)
    limit_percentage = models.FloatField(null=False)
    stop_percentage = models.FloatField(null=False)

    class Meta:
        unique_together = ['name', 'contract']
        verbose_name_plural = 'Strategies'

    def __str__(self):
        return (f'{self.name} :: {self.contract} '
                f'- Side :: {self.side} '
                f'- Quantity :: {self.quantity} '
                f'- Limit :: {self.limit_percentage}'
                f'- Stop :: {self.stop_percentage}')


class Price(models.Model):
    con_id = models.CharField('Contract Id', max_length=16, db_index=True)
    update_time = models.DateTimeField(null=False)
    last = models.FloatField(null=False)
    bid = models.FloatField(null=False)
    ask = models.FloatField(null=False)

    class Meta:
        unique_together = ['con_id', 'update_time']
        verbose_name_plural = 'Prices'

    def __str__(self):
        return (f'{self.con_id} :: {self.update_time} '
                f'- Last :: {self.last} '
                f'- Bid :: {self.bid} '
                f'- Ask :: {self.ask}')


class Order(models.Model):
    account_id = models.CharField(max_length=64, blank=False, null=False)
    con_id = models.CharField('Contract Id', max_length=16, blank=False, null=False)
    parent_id = models.CharField(max_length=16, blank=True, null=True)
    order_id = models.CharField(max_length=16, blank=False, null=False)
    order_ref = models.CharField(max_length=16, blank=True, null=True)
    order_description = models.CharField(max_length=128, blank=True, null=True)
    last_execution_time = models.DateTimeField(null=False)
    side = models.CharField(max_length=4, blank=False, null=False)
    order_type = models.CharField(max_length=16, blank=False, null=False)
    status = models.CharField(max_length=16, blank=False, null=False)
    total_size = models.FloatField(null=True)
    price = models.FloatField(null=True)
    avg_price = models.FloatField(null=True)
    stop_price = models.FloatField(null=True)

    class Meta:
        unique_together = ['account_id', 'order_id']
        verbose_name_plural = 'Orders'

    def __str__(self):
        return (f'{self.con_id} :: {self.side} :: {self.order_type} :: {self.last_execution_time} '
                f'- Parent :: {self.parent_id} '
                f'- Order :: {self.order_id} '
                f'- Status :: {self.status}')
