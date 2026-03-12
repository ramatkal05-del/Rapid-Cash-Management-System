from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
from core.models import Currency, User
from operations.models import Caisse, Operation, FeeGrid
from operations.services import OperationService

User = get_user_model()

class OperationServiceTest(TestCase):
    def setUp(self):
        # Create test data
        self.usd = Currency.objects.create(code='USD', name='US Dollar', is_reference=True)
        self.eur = Currency.objects.create(code='EUR', name='Euro')
        
        # Create fee grid
        FeeGrid.objects.create(
            min_amount=0.10, max_amount=40.00, fee_amount=5.00, currency=self.usd
        )
        
        # Create admin user
        self.admin = User.objects.create_user(
            username='admin', password='test123', role='ADMIN'
        )
        
        # Create agent
        self.agent = User.objects.create_user(
            username='agent', password='test123', role='AGENT'
        )
        
        # Create caisse
        self.caisse = Caisse.objects.create(
            name='Main Caisse', agent=self.agent, balance=Decimal('1000.00'), currency=self.usd
        )

    def test_create_operation_success(self):
        """Test successful operation creation"""
        operation = OperationService.create_operation(
            agent=self.agent,
            op_type='TRANSFER',
            caisse_id=self.caisse.id,
            amount_orig=Decimal('100.00'),
            currency_orig_id=self.usd.id,
            observation='Test operation'
        )
        
        self.assertEqual(operation.type, 'TRANSFER')
        self.assertEqual(operation.amount_orig, Decimal('100.00'))
        self.assertEqual(operation.agent, self.agent)
        self.assertEqual(operation.status, 'COMPLETED')
        
        # Check caisse balance updated
        self.caisse.refresh_from_db()
        self.assertEqual(self.caisse.balance, Decimal('900.00'))

    def test_create_operation_insufficient_funds(self):
        """Test operation creation with insufficient funds"""
        with self.assertRaises(Exception) as context:
            OperationService.create_operation(
                agent=self.agent,
                op_type='TRANSFER',
                caisse_id=self.caisse.id,
                amount_orig=Decimal('2000.00'),
                currency_orig_id=self.usd.id,
            )
        
        self.assertIn('Insufficient funds', str(context.exception))

    def test_fee_calculation(self):
        """Test automatic fee calculation"""
        operation = OperationService.create_operation(
            agent=self.agent,
            op_type='TRANSFER',
            caisse_id=self.caisse.id,
            amount_orig=Decimal('50.00'),
            currency_orig_id=self.usd.id,
        )
        
        # Should be in the 40.10-100.00 range, fee = 8.00
        self.assertEqual(operation.fee_calculated, Decimal('8.00'))

class OperationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_user(
            username='admin', password='test123', role='ADMIN'
        )
        self.agent = User.objects.create_user(
            username='agent', password='test123', role='AGENT'
        )
        self.client.login(username='admin', password='test123')

    def test_dashboard_view(self):
        """Test dashboard view loads correctly"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'dashboard')

    def test_agents_list_admin_only(self):
        """Test agents list is accessible only to admin"""
        response = self.client.get(reverse('agents_list'))
        self.assertEqual(response.status_code, 200)
        
        # Logout admin and login as agent
        self.client.logout()
        self.client.login(username='agent', password='test123')
        
        response = self.client.get(reverse('agents_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to dashboard
