"""
Rapid Cash - API Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from core.models import User, Currency, ExchangeRate, AuditLog
from core.serializers import (
    UserSerializer, CurrencySerializer,
    ExchangeRateSerializer, AuditLogSerializer
)
from operations.models import Operation, Caisse, FeeGrid
from operations.serializers import (
    OperationSerializer, OperationCreateSerializer,
    CaisseSerializer, FeeGridSerializer
)
from operations.services import OperationService


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=user.id)


class CurrencyViewSet(viewsets.ModelViewSet):
    """API endpoint for currencies"""
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    permission_classes = [IsAuthenticated]


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


class OperationViewSet(viewsets.ModelViewSet):
    """API endpoint for operations"""
    serializer_class = OperationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Operation.objects.all()
        
        # Filter by user role
        if user.role != 'ADMIN':
            queryset = queryset.filter(agent=user)
        
        # Apply filters
        op_type = self.request.query_params.get('type')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if op_type:
            queryset = queryset.filter(type=op_type)
        if date_from:
            queryset = queryset.filter(date_time__date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date_time__date__lte=date_to)
        
        return queryset.select_related(
            'agent', 'caisse', 'currency_orig', 'currency_ref'
        ).order_by('-date_time')
    
    def create(self, request, *args, **kwargs):
        """Create a new operation via API"""
        serializer = OperationCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            operation = OperationService.create_operation(
                agent=request.user,
                op_type=serializer.validated_data['type'],
                caisse_id=serializer.validated_data['caisse'].id,
                amount_orig=serializer.validated_data['amount_orig'],
                currency_orig_id=serializer.validated_data['currency_orig'].id,
                observation=serializer.validated_data.get('observation', '')
            )
            
            return Response(
                OperationSerializer(operation).data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get operation statistics"""
        user = request.user
        today = timezone.now().date()
        
        operations = Operation.objects.filter(date_time__date=today)
        if user.role != 'ADMIN':
            operations = operations.filter(agent=user)
        
        return Response({
            'date': str(today),
            'count': operations.count(),
            'total_volume': operations.aggregate(Sum('amount_ref'))['amount_ref__sum'] or 0,
            'total_fees': operations.aggregate(Sum('fee_calculated'))['fee_calculated__sum'] or 0,
        })


class CaisseViewSet(viewsets.ModelViewSet):
    """API endpoint for caisses"""
    serializer_class = CaisseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Caisse.objects.all()
        
        if user.role != 'ADMIN':
            queryset = queryset.filter(agent=user)
        
        return queryset.select_related('agent', 'currency')


class FeeGridViewSet(viewsets.ModelViewSet):
    """API endpoint for fee grids"""
    queryset = FeeGrid.objects.all()
    serializer_class = FeeGridSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        currency = self.request.query_params.get('currency')
        queryset = FeeGrid.objects.all()
        
        if currency:
            queryset = queryset.filter(currency__code=currency)
        
        return queryset.select_related('currency')


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
        
        # Filters
        action = self.request.query_params.get('action')
        model = self.request.query_params.get('model')
        
        if action:
            queryset = queryset.filter(action=action)
        if model:
            queryset = queryset.filter(model_name=model)
        
        return queryset.select_related('user')[:1000]  # Limit to 1000


# Import User at module level
from django.contrib.auth import get_user_model
User = get_user_model()
