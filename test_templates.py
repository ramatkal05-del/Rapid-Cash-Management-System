#!/usr/bin/env python
"""
Script de test des templates pour vérifier la syntaxe Django
"""

import os
import sys
import re

def test_template_syntax():
    """Tester la syntaxe des templates Django"""
    
    print("🔍 TEST SYNTAXE TEMPLATES DJANGO")
    print("=" * 50)
    
    # Patterns à vérifier
    problematic_patterns = [
        (r':\d+d', 'Formatage Python (ex: month:02d)'),
        (r':\.\d+f', 'Formatage Python (ex: amount:.2f)'),
        (r':[^}]+', 'Formatage Python potentiel'),
    ]
    
    # Templates à vérifier
    template_dir = 'templates'
    checked_files = 0
    issues_found = 0
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                checked_files += 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    file_issues = []
                    
                    for pattern, description in problematic_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            file_issues.extend(matches)
                    
                    if file_issues:
                        issues_found += 1
                        print(f"\n❌ {file_path}")
                        for issue in file_issues:
                            print(f"   Problème: {issue}")
                    else:
                        print(f"✅ {file_path}")
                        
                except Exception as e:
                    print(f"⚠️ {file_path} - Erreur lecture: {e}")
    
    print(f"\n📊 RÉSULTATS:")
    print(f"   Fichiers vérifiés: {checked_files}")
    print(f"   Fichiers avec problèmes: {issues_found}")
    
    if issues_found == 0:
        print("🎉 Tous les templates sont corrects !")
    else:
        print("⚠️ Certains templates ont des problèmes de syntaxe")
    
    print("\n💡 SYNTAXE CORRECTE DJANGO:")
    print("   ❌ mauvais: {{ month:02d }}")
    print("   ✅ bon:    {{ month|stringformat:\"02d\" }}")
    print("   ❌ mauvais: {{ amount:.2f }}")
    print("   ✅ bon:    {{ amount|floatformat:2 }}")

if __name__ == '__main__':
    test_template_syntax()
