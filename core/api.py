"""
Rapid Cash - Core API Views
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Currency, ExchangeRate, AuditLog
from core.serializers import (
    CurrencySerializer, ExchangeRateSerializer, AuditLogSerializer
)
from django.contrib.auth import get_user_model
User = get_user_model()


class CurrencyViewSet(viewsets.ModelViewSet):
    """API endpoint for currencies"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return super().get_permissions()


class ExchangeRateViewSet(viewsets.ModelViewSet):
    """API endpoint for exchange rates"""
    queryset = ExchangeRate.objects.all()
    serializer_class = ExchangeRateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        base = self.request.query_params.get('base')
        target = self.request.query_params.get('target')
        
        queryset = ExchangeRate.objects.all()
        
        if base:
            queryset = queryset.filter(base_currency__code=base)
        if target:
            queryset = queryset.filter(target_currency__code=target)
            
        return queryset.select_related('base_currency', 'target_currency')


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for audit logs"""
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = AuditLog.objects.all()
        
        # Admin sees all, others see their own
        if user.role != 'ADMIN':
            queryset = queryset.filter(user=user)
        
        return queryset.select_related('user')[:500]
