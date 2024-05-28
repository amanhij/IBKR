from django.db import models

from .models_types import PositionStatus, Strategy


class Contract(models.Model):
    conid = models.CharField("Contract Id", max_length=64, blank=False, null=False)
    name = models.CharField(max_length=64, blank=False, null=False)


class Price(models.Model):
    conid = models.CharField("Contract Id", max_length=64, db_index=True)
    update_time = models.DateTimeField(null=False)
    last = models.FloatField(null=False)
    bid = models.FloatField(null=True)
    ask = models.FloatField(null=True)

    class Meta:
        unique_together = ['conid', 'update_time']
        verbose_name_plural = "Prices"

    def __str__(self):
        return f"{self.conid} :: {self.update_time} - Last :: {self.last} - Bid:: {self.bid} - Ask {self.ask} "


class Position(models.Model):
    strategy = models.CharField("Strategy", max_length=64, choices=Strategy.choices, default=Strategy.CLEMENCE)
    trade_id = models.CharField("Reference ID", null=True, default=None, editable=False, max_length=64, db_index=True)
    status = models.CharField("Status", max_length=64, choices=PositionStatus.choices, default=PositionStatus.OPEN)
    open_date = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    closed_date = models.DateTimeField(null=True, blank=True)
    size = models.FloatField(null=True, blank=True)
    entry_price = models.FloatField(null=True, blank=True)
    profit_loss = models.FloatField(null=True, blank=True)
    sold_price = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Positions"

    def __str__(self):
        return f"{self.strategy} - Trading ID: {self.trade_id} - Status: {self.status}"
