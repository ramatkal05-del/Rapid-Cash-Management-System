from django.contrib import admin
from .models import FeeGrid, Caisse, Operation

@admin.register(FeeGrid)
class FeeGridAdmin(admin.ModelAdmin):
    list_display = ('min_amount', 'max_amount', 'fee_amount', 'currency')
    list_filter = ('currency',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form

@admin.register(Caisse)
class CaisseAdmin(admin.ModelAdmin):
    list_display = ('name', 'agent', 'balance', 'currency')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form

@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('transaction_number', 'type', 'amount_orig', 'currency_orig', 'agent', 'date_time')
    list_filter = ('type', 'agent', 'currency_orig')
    readonly_fields = ('transaction_number', 'date_time')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form
