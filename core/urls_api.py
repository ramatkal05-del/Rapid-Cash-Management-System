"""
Rapid Cash - Core API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core.api import CurrencyViewSet, ExchangeRateViewSet, AuditLogViewSet

router = DefaultRouter()
router.register(r'currencies', CurrencyViewSet, basename='currency')
router.register(r'exchange-rates', ExchangeRateViewSet, basename='exchangerate')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
]
