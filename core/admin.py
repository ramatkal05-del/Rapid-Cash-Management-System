from django.contrib import admin
from django.utils.html import mark_safe
from .models import User, Currency, ExchangeRate

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # S'assurer que le formulaire utilise UTF-8
        form.encoding = 'utf-8'
        return form

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'symbol', 'is_reference')
    list_filter = ('is_reference',)
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('base_currency', 'target_currency', 'rate', 'date_updated')
    list_filter = ('base_currency', 'target_currency')
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.encoding = 'utf-8'
        return form
