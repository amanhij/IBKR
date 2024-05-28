from .models import *

admin.site.site_title = 'Cryptalis | BOT'
admin.site.site_header = 'Cryptalis | BOT'
admin.site.index_title = None
admin.site.site_url = None

admin.site.register(Contract, ContractView)
admin.site.register(Price, PriceView)
admin.site.register(Position, PositionView)
