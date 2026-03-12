#!/usr/bin/env python
"""
Test simple pour vérifier que le template capital_management fonctionne
"""

import os
import sys

def test_template():
    """Test simple du template"""
    
    print("🧪 TEST TEMPLATE capital_management.html")
    print("=" * 40)
    
    template_path = 'templates/core/capital_management.html'
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Vérifier que les patterns problématiques n'existent plus
        problematic_patterns = [
            'month:02d',
            'year:',  # Pas de formatage direct
            ':02d',
            ':.2f',
        ]
        
        issues = []
        for pattern in problematic_patterns:
            if pattern in content:
                issues.append(f"Trouvé: {pattern}")
        
        # Vérifier que les patterns corrects existent
        correct_patterns = [
            'stringformat:"02d"',
            'floatformat:2',
        ]
        
        found_correct = []
        for pattern in correct_patterns:
            if pattern in content:
                found_correct.append(f"✅ {pattern}")
        
        print(f"📁 Fichier: {template_path}")
        print(f"📏 Taille: {len(content)} caractères")
        
        if issues:
            print("\n❌ Problèmes trouvés:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("\n✅ Aucun problème de formatage trouvé")
        
        if found_correct:
            print("\n🎯 Patterns corrects trouvés:")
            for pattern in found_correct:
                print(f"   {pattern}")
        
        # Afficher les lignes avec les dates formatées
        print("\n📋 Lignes avec formatage de dates:")
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if 'stringformat' in line or 'month' in line and '{{' in line:
                print(f"   Ligne {i}: {line.strip()}")
        
        print("\n🎉 Test terminé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    test_template()
