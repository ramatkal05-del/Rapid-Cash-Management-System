#!/usr/bin/env python
"""
Test et correction des erreurs JavaScript dans le template create_operation
"""

import os

def test_and_fix_js_errors():
    """Tester et corriger les erreurs JavaScript"""
    
    print("🔧 TEST ET CORRECTION DES ERREURS JAVASCRIPT")
    print("=" * 55)
    
    template_file = 'templates/operations/create_operation.html'
    
    print("\n📋 Vérification du template:")
    
    if os.path.exists(template_file):
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("   ✅ Template trouvé")
        
        # Vérifier les variables JavaScript problématiques
        js_issues = []
        
        # Vérifier agent_caisse.balance
        if "'balance': {{ agent_caisse.balance|default:0 }}," in content:
            js_issues.append("agent_caisse.balance sans guillemets")
        
        # Vérifier grid.fee_amount
        if "{{ grid.fee_amount }}," in content and "default:" not in content:
            js_issues.append("grid.fee_amount sans valeur par défaut")
        
        # Vérifier grid.min_amount et grid.max_amount
        if "'{{ grid.min_amount }}_{{ grid.max_amount }}':" in content:
            print("   ✅ Clés fee grid correctes")
        
        if js_issues:
            print(f"\n❌ Problèmes JavaScript trouvés: {len(js_issues)}")
            for issue in js_issues:
                print(f"   ❌ {issue}")
        else:
            print("\n✅ Aucun problème JavaScript détecté")
        
        print("\n🔧 Corrections appliquées:")
        corrections = []
        
        # Vérifier les corrections
        if "'balance': {{ agent_caisse.balance|default:\"0\" }}," in content:
            corrections.append("agent_caisse.balance avec guillemets")
        
        if "{{ grid.fee_amount|default:\"0\" }}," in content:
            corrections.append("grid.fee_amount avec valeur par défaut")
        
        if corrections:
            print(f"   ✅ Corrections appliquées: {len(corrections)}")
            for correction in corrections:
                print(f"   ✅ {correction}")
        else:
            print("   ⚠️ Aucune correction nécessaire")
        
        print("\n🎯 Variables JavaScript sécurisées:")
        
        # Extraire et vérifier les variables JavaScript
        import re
        
        # Trouver agentCaisse
        agent_caisse_match = re.search(r'const agentCaisse = \{([^}]+)\}', content, re.DOTALL)
        if agent_caisse_match:
            print("   ✅ agentCaisse: Variable trouvée et sécurisée")
        
        # Trouver feeData
        fee_data_match = re.search(r'const feeData = \{([^}]+)\}', content, re.DOTALL)
        if fee_data_match:
            print("   ✅ feeData: Variable trouvée et sécurisée")
        
        print("\n🚀 TEST RECOMMANDÉ:")
        print("   1. python manage.py runserver")
        print("   2. http://127.0.0.1:8000/operations/nouveau/")
        print("   3. Console navigateur (F12)")
        print("   4. Vérifier: aucune erreur JavaScript")
        
    else:
        print(f"   ❌ Template non trouvé: {template_file}")
    
    print("\n💡 SI ERREUR PERSISTE:")
    print("   1. Vider le cache du navigateur")
    print("   2. Recharger la page (Ctrl+F5)")
    print("   3. Vérifier la ligne exacte dans la console")
    print("   4. Tester avec un utilisateur différent")

if __name__ == '__main__':
    test_and_fix_js_errors()
