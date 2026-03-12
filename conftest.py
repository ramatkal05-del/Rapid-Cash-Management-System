"""
Pytest configuration and fixtures for Rapid Cash
"""
import pytest
from decimal import Decimal
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def db_access_without_rollback_and_truncate(request, django_db_setup, django_db_blocker):
    """Allow database access for tests that need it"""
    django_db_blocker.unblock()
    request.addfinalizer(django_db_blocker.restore)


@pytest.fixture
def admin_user(db):
    """Create an admin user"""
    return User.objects.create_user(
        username='admin',
        email='admin@test.com',
        password='testpass123',
        role=User.Role.ADMIN,
        is_staff=True
    )


@pytest.fixture
def agent_user(db):
    """Create an agent user"""
    return User.objects.create_user(
        username='agent',
        email='agent@test.com',
        password='testpass123',
        role=User.Role.AGENT,
        commission_rate=Decimal('10.00')
    )


@pytest.fixture
def api_client():
    """Return an API client"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, admin_user):
    """Return an authenticated API client"""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def currency_usd(db):
    """Create USD currency"""
    from core.models import Currency
    return Currency.objects.create(
        code='USD',
        name='US Dollar',
        symbol='$',
        is_reference=True
    )


@pytest.fixture
def currency_cdf(db):
    """Create CDF currency"""
    from core.models import Currency
    return Currency.objects.create(
        code='CDF',
        name='Congolese Franc',
        symbol='FC'
    )


@pytest.fixture
def fee_grid_usd(db, currency_usd):
    """Create fee grid for USD"""
    from operations.models import FeeGrid
    return FeeGrid.objects.create(
        min_amount=Decimal('0.10'),
        max_amount=Decimal('40.00'),
        fee_amount=Decimal('5.00'),
        currency=currency_usd
    )


@pytest.fixture
def caisse_usd(db, agent_user, currency_usd):
    """Create a USD caisse"""
    from operations.models import Caisse
    return Caisse.objects.create(
        name='Caisse Principale USD',
        agent=agent_user,
        balance=Decimal('1000.00'),
        currency=currency_usd
    )
