"""
Rapid Cash - API Serializers
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from core.models import Currency, ExchangeRate, AuditLog

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'phone', 'commission_rate',
            'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']


class CurrencySerializer(serializers.ModelSerializer):
    """Serializer for Currency model"""
    
    class Meta:
        model = Currency
        fields = ['id', 'code', 'name', 'symbol', 'is_reference']


class ExchangeRateSerializer(serializers.ModelSerializer):
    """Serializer for ExchangeRate model"""
    base_currency_code = serializers.CharField(source='base_currency.code', read_only=True)
    target_currency_code = serializers.CharField(source='target_currency.code', read_only=True)
    
    class Meta:
        model = ExchangeRate
        fields = [
            'id', 'base_currency', 'base_currency_code',
            'target_currency', 'target_currency_code',
            'rate', 'date_updated'
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'action', 'action_display', 'user', 'user_username',
            'model_name', 'object_id', 'object_repr', 'changes',
            'ip_address', 'timestamp'
        ]
