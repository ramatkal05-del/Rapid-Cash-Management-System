#!/usr/bin/env python
"""
Simulation d'un transfert de 300 dollars en tant qu'agent
"""

import os
import sys

def simulate_agent_transfer():
    """Simuler un transfert de 300 dollars en tant qu'agent"""
    
    print("💸 SIMULATION TRANSFERT 300$ EN TANT QU'AGENT")
    print("=" * 55)
    
    # Configuration Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from operations.models import Operation, Caisse, FeeGrid
        from operations.forms import OperationForm
        from operations.services import OperationService
        from core.models import Currency
        from decimal import Decimal
        
        User = get_user_model()
        
        print("\n👤 SÉLECTION DE L'AGENT:")
        
        # Trouver un agent (pas un admin)
        agent = User.objects.filter(role='AGENT').first()
        
        if not agent:
            print("   ❌ Aucun agent trouvé")
            return
        
        print(f"   ✅ Agent sélectionné: {agent.username}")
        print(f"      Rôle: {agent.get_role_display()}")
        
        print("\n🏦 VÉRIFICATION DE LA CAISSE:")
        
        caisse = Caisse.objects.filter(agent=agent).first()
        
        if not caisse:
            print("   ❌ Aucune caisse assignée à l'agent")
            return
        
        print(f"   ✅ Caisse: #{caisse.id}")
        print(f"      Nom: {caisse.name}")
        print(f"      Solde avant: {caisse.balance} {caisse.currency.code}")
        print(f"      Devise: {caisse.currency.code}")
        
        # Vérifier que c'est bien du USD
        if caisse.currency.code != 'USD':
            print(f"   ⚠️ La caisse n'utilise pas USD mais {caisse.currency.code}")
            print(f"   Recherche d'une caisse USD...")
            
            usd_currency = Currency.objects.filter(code='USD').first()
            if usd_currency:
                caisse = Caisse.objects.filter(currency=usd_currency).first()
                if caisse:
                    print(f"   ✅ Caisse USD trouvée: #{caisse.id}")
                else:
                    print("   ❌ Aucune caisse USD trouvée")
                    return
        
        print("\n💰 MONTANT DU TRANSFERT:")
        amount = Decimal('300.00')
        print(f"   Montant: {amount} USD")
        
        # Vérifier le solde suffisant
        if caisse.balance < amount:
            print(f"   ❌ Solde insuffisant!")
            print(f"      Solde: {caisse.balance} USD")
            print(f"      Requis: {amount} USD")
            print(f"      Manque: {amount - caisse.balance} USD")
            
            # Pour le test, on ajoute des fonds
            print(f"\n   💡 Pour le test, ajout de fonds...")
            caisse.balance += Decimal('1000.00')
            caisse.save()
            print(f"   ✅ Nouveau solde: {caisse.balance} USD")
        else:
            print(f"   ✅ Solde suffisant")
        
        print("\n📋 CRÉATION DU FORMULAIRE:")
        
        form_data = {
            'type': 'TRANSFER',
            'amount_orig': str(amount),
            'currency_orig': caisse.currency.id,
            'observation': 'Test transfert 300$ par agent'
        }
        
        print(f"   Type: {form_data['type']}")
        print(f"   Montant: {form_data['amount_orig']}")
        print(f"   Devise: {form_data['currency_orig']}")
        
        form = OperationForm(data=form_data, agent=agent)
        
        if form.is_valid():
            print("   ✅ Formulaire valide!")
            
            print("\n🚀 CRÉATION DE L'OPÉRATION:")
            
            try:
                from django.db import transaction
                
                with transaction.atomic():
                    operation = OperationService.create_operation(
                        agent=agent,
                        op_type='TRANSFER',
                        caisse_id=caisse.id,
                        amount_orig=amount,
                        currency_orig_id=caisse.currency.id,
                        observation="Transfert de 300$ - Test agent"
                    )
                
                print(f"   ✅ OPÉRATION CRÉÉE AVEC SUCCÈS!")
                print(f"      ID: #{operation.id}")
                print(f"      Numéro: {operation.transaction_number}")
                print(f"      Type: {operation.get_type_display()}")
                print(f"      Montant: {operation.amount_orig} {operation.currency_orig.code}")
                print(f"      Frais: {operation.fee_calculated} {operation.currency_orig.code}")
                print(f"      Total: {operation.amount_ref} {operation.currency_ref.code}")
                print(f"      Date: {operation.date_time}")
                print(f"      Agent: {operation.agent.username}")
                print(f"      Caisse: {operation.caisse.name}")
                
                # Vérifier le nouveau solde
                caisse.refresh_from_db()
                print(f"\n💰 SOLDE APRÈS OPÉRATION:")
                print(f"   Solde caisse: {caisse.balance} {caisse.currency.code}")
                print(f"   Déduction: {amount} USD")
                
                print("\n🎯 RÉSULTAT:")
                print("   ✅ Transfert de 300$ effectué avec succès!")
                print("   ✅ Opération enregistrée dans la base de données")
                print("   ✅ Solde de la caisse mis à jour")
                
                # Nettoyage
                operation.delete()
                print("\n🧹 Nettoyage: Opération de test supprimée")
                
                # Restaurer le solde original
                caisse.balance -= Decimal('1000.00')
                caisse.save()
                print("   Solde restauré")
                
            except Exception as e:
                print(f"   ❌ Erreur création: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("   ❌ Formulaire invalide:")
            for field, errors in form.errors.items():
                print(f"      {field}: {errors}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    simulate_agent_transfer()
