from django.contrib import admin


class ContractView(admin.ModelAdmin):
    list_display = ['conid', 'name']


class PriceView(admin.ModelAdmin):
    list_display = ['conid', 'update_time', 'last', 'bid', 'ask', ]
    list_filter = ['conid', 'update_time']
    search_fields = ('conid', 'update_time')
    sortable_by = ['conid', 'update_time']

    def has_add_permission(self, request, obj=None):
        return False


class PositionView(admin.ModelAdmin):
    list_display = ['strategy', 'trade_id', 'status',
                    'open_date', 'closed_date', 'size',
                    'entry_price', 'profit_loss', 'sold_price']
    list_filter = ['strategy', 'status', 'open_date', 'closed_date']
    search_fields = ('trade_id', 'status')
    fields = ['strategy', 'status', 'open_date', 'closed_date']
    sortable_by = ['status', 'open_date', 'closed_date']

    def has_add_permission(self, request, obj=None):
        return False
