"""
Rapid Cash - API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from operations.api import (
    OperationViewSet, CaisseViewSet, FeeGridViewSet,
    AuditLogViewSet
)

router = DefaultRouter()
router.register(r'operations', OperationViewSet, basename='operation')
router.register(r'caisses', CaisseViewSet, basename='caisse')
router.register(r'fee-grids', FeeGridViewSet, basename='feegrid')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('', include(router.urls)),
]
