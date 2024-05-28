from django.db import models


class Strategy(models.TextChoices):
    CLEMENCE = 'CLÉMENCE', 'CLÉMENCE'
    CLEMENTINE = 'CLEMENTINE', 'CLEMENTINE'


class PositionStatus(models.TextChoices):
    OPEN = 'OPEN', 'OPEN'
    CLOSED = 'CLOSED', 'CLOSED'
    REJECTED = 'REJECTED', 'REJECTED'
