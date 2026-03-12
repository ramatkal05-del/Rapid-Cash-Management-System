from django.contrib import admin
from .models import Expense, PartnerContract, PartnerPayment

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'reason', 'amount', 'currency', 'category', 'admin')
    list_filter = ('category', 'admin', 'date')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form

@admin.register(PartnerContract)
class PartnerContractAdmin(admin.ModelAdmin):
    list_display = ('partner', 'type', 'amount_engaged', 'currency', 'status')
    list_filter = ('type', 'status')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form

@admin.register(PartnerPayment)
class PartnerPaymentAdmin(admin.ModelAdmin):
    list_display = ('contract', 'date', 'amount', 'currency')
    list_filter = ('date',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form
