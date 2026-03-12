"""
Tests for Operations API
"""
import pytest
from decimal import Decimal
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.django_db


class TestCurrencyAPI:
    """Test currency API endpoints"""
    
    def test_list_currencies(self, authenticated_client, currency_usd):
        """Test listing currencies"""
        response = authenticated_client.get('/api/core/currencies/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1
    
    def test_create_currency(self, authenticated_client):
        """Test creating a currency"""
        data = {
            'code': 'EUR',
            'name': 'Euro',
            'symbol': '€',
            'is_reference': False
        }
        response = authenticated_client.post('/api/core/currencies/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['code'] == 'EUR'


class TestExchangeRateAPI:
    """Test exchange rate API endpoints"""
    
    def test_list_exchange_rates(self, authenticated_client, currency_usd, currency_cdf):
        """Test listing exchange rates"""
        from core.models import ExchangeRate
        ExchangeRate.objects.create(
            base_currency=currency_usd,
            target_currency=currency_cdf,
            rate=Decimal('2800.00')
        )
        response = authenticated_client.get('/api/core/exchange-rates/')
        assert response.status_code == status.HTTP_200_OK


class TestOperationAPI:
    """Test operation API endpoints"""
    
    def test_list_operations(self, authenticated_client):
        """Test listing operations"""
        response = authenticated_client.get('/api/operations/operations/')
        assert response.status_code == status.HTTP_200_OK
    
    def test_create_operation(self, authenticated_client, currency_usd, fee_grid_usd, caisse_usd):
        """Test creating an operation"""
        data = {
            'type': 'TRANSFER',
            'amount_orig': '100.00',
            'currency_orig': currency_usd.id,
            'caisse': caisse_usd.id,
            'observation': 'Test transfer'
        }
        response = authenticated_client.post('/api/operations/operations/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert 'transaction_number' in response.data
    
    def test_operation_stats(self, authenticated_client, agent_user, currency_usd, fee_grid_usd, caisse_usd):
        """Test getting operation statistics"""
        # Create test operation
        from operations.models import Operation
        Operation.objects.create(
            transaction_number='TEST001',
            agent=agent_user,
            caisse=caisse_usd,
            type='TRANSFER',
            amount_orig=Decimal('100.00'),
            currency_orig=currency_usd,
            amount_ref=Decimal('100.00'),
            currency_ref=currency_usd,
            exchange_rate=Decimal('1.00'),
            fee_calculated=Decimal('5.00')
        )
        
        response = authenticated_client.get('/api/operations/operations/stats/')
        assert response.status_code == status.HTTP_200_OK
        assert 'count' in response.data


class TestCaisseAPI:
    """Test caisse API endpoints"""
    
    def test_list_caisses(self, authenticated_client, caisse_usd):
        """Test listing caisses"""
        response = authenticated_client.get('/api/operations/caisses/')
        assert response.status_code == status.HTTP_200_OK


class TestFeeGridAPI:
    """Test fee grid API endpoints"""
    
    def test_list_fee_grids(self, authenticated_client, fee_grid_usd):
        """Test listing fee grids"""
        response = authenticated_client.get('/api/operations/fee-grids/')
        assert response.status_code == status.HTTP_200_OK
