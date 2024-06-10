from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin

from core.models import Price, Order


class ContractView(admin.ModelAdmin):
    list_display = ['con_id', 'name']


class StrategyView(admin.ModelAdmin):
    list_display = ['name', 'contract', 'side', 'account_id', 'quantity', 'limit_factor', 'stop_factor']
    list_filter = ['name', 'contract', 'side', 'account_id']
    search_fields = ('name', 'contract', 'side', 'account_id')
    sortable_by = ['name', 'contract', 'side', 'account_id']


class PriceResource(resources.ModelResource):
    class Meta:
        model = Price


class PriceView(ExportMixin, admin.ModelAdmin):
    list_display = ['con_id', 'update_time', 'last', 'bid', 'ask', ]
    list_filter = ['con_id', 'update_time']
    search_fields = ('con_id', 'update_time')
    sortable_by = ['con_id', 'update_time']
    readonly_fields = ['con_id', 'update_time', 'last', 'bid', 'ask', ]

    def has_add_permission(self, request, obj=None):
        return False


class OrderResource(resources.ModelResource):
    class Meta:
        model = Order


class OrderView(ExportMixin, admin.ModelAdmin):
    list_display = ['order_id', 'parent_id', 'last_execution_time',
                    'side', 'order_type', 'status', 'ccp_status',
                    'total_size', 'price', 'stop_price']
    list_filter = ['last_execution_time', 'side', 'order_type', 'status']
    search_fields = ('last_execution_time', 'side', 'order_type', 'status')
    sortable_by = ['order_id', 'last_execution_time']
    readonly_fields = ['account_id', 'con_id', 'parent_id', 'order_id', 'order_ref', 'order_description',
                       'last_execution_time', 'side', 'order_type', 'status', 'ccp_status', 'total_size', 'price', 'avg_price', 'stop_price']

    def get_ordering(self, request):
        return ['-last_execution_time']  #

    def has_add_permission(self, request, obj=None):
        return False
