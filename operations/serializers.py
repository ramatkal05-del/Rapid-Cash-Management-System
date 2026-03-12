"""
Rapid Cash - Operations API Serializers
"""
from rest_framework import serializers
from operations.models import Operation, Caisse, FeeGrid


class FeeGridSerializer(serializers.ModelSerializer):
    """Serializer for FeeGrid model"""
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    
    class Meta:
        model = FeeGrid
        fields = ['id', 'min_amount', 'max_amount', 'fee_amount', 'currency', 'currency_code']


class CaisseSerializer(serializers.ModelSerializer):
    """Serializer for Caisse model"""
    agent_name = serializers.CharField(source='agent.username', read_only=True)
    currency_code = serializers.CharField(source='currency.code', read_only=True)
    
    class Meta:
        model = Caisse
        fields = ['id', 'name', 'agent', 'agent_name', 'balance', 'currency', 'currency_code']


class OperationSerializer(serializers.ModelSerializer):
    """Serializer for Operation model"""
    agent_name = serializers.CharField(source='agent.username', read_only=True)
    caisse_name = serializers.CharField(source='caisse.name', read_only=True)
    currency_orig_code = serializers.CharField(source='currency_orig.code', read_only=True)
    currency_ref_code = serializers.CharField(source='currency_ref.code', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    
    class Meta:
        model = Operation
        fields = [
            'id', 'transaction_number', 'date_time', 'agent', 'agent_name',
            'caisse', 'caisse_name', 'type', 'type_display',
            'amount_orig', 'currency_orig', 'currency_orig_code',
            'amount_ref', 'currency_ref', 'currency_ref_code',
            'exchange_rate', 'fee_calculated', 'observation', 'status'
        ]
        read_only_fields = ['id', 'transaction_number', 'date_time', 'exchange_rate', 'fee_calculated', 'status']


class OperationCreateSerializer(serializers.Serializer):
    """Serializer for creating operations"""
    type = serializers.ChoiceField(choices=Operation.Type.choices)
    amount_orig = serializers.DecimalField(max_digits=20, decimal_places=2)
    currency_orig = serializers.PrimaryKeyRelatedField(queryset=Operation._meta.get_field('currency_orig').remote_field.model.objects.all())
    caisse = serializers.PrimaryKeyRelatedField(queryset=Caisse.objects.all())
    observation = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        """Validate operation data"""
        if data['amount_orig'] <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return data
