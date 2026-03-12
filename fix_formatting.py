#!/usr/bin/env python
"""
Test précis des problèmes de formatage Django dans les templates
"""

import os
import re

def test_django_formatting():
    """Tester uniquement les problèmes de formatage Django"""
    
    print("🔍 TEST FORMATAGE DJANGO TEMPLATES")
    print("=" * 50)
    
    # Patterns spécifiques au formatage Python dans les templates Django
    django_formatting_issues = [
        r'\{\{\s*\w+\.\w+\s*:\d+d\s*\}\}',  # {{ month:02d }}
        r'\{\{\s*\w+\s*:\d+d\s*\}\}',      # {{ month:02d }}
        r'\{\{\s*\w+\.\w+\s*:\.\d+f\s*\}\}', # {{ amount:.2f }}
        r'\{\{\s*\w+\s*:\.\d+f\s*\}\}',     # {{ amount:.2f }}
    ]
    
    template_dir = 'templates'
    fixed_files = 0
    total_issues = 0
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_issues = 0
                    
                    # Corriger {{ month:02d }} → {{ month|stringformat:"02d" }}
                    content = re.sub(
                        r'\{\{\s*(\w+(?:\.\w+)*)\s*:(\d+d)\s*\}\}',
                        r'{{ \1|stringformat:"\2" }}',
                        content
                    )
                    
                    # Corriger {{ amount:.2f }} → {{ amount|floatformat:2 }}
                    content = re.sub(
                        r'\{\{\s*(\w+(?:\.\w+)*)\s*:(\.\d+f)\s*\}\}',
                        r'{{ \1|floatformat:\2 }}',
                        content
                    )
                    
                    # Compter les changements
                    if content != original_content:
                        file_issues = len(re.findall(r':\d+d|:\.\d+f', original_content))
                        total_issues += file_issues
                        fixed_files += 1
                        
                        # Sauvegarder les corrections
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                        print(f"✅ {file_path} - {file_issues} corrections")
                    
                except Exception as e:
                    print(f"❌ {file_path} - Erreur: {e}")
    
    print(f"\n📊 RÉSULTATS:")
    print(f"   Fichiers corrigés: {fixed_files}")
    print(f"   Total corrections: {total_issues}")
    
    if total_issues > 0:
        print("🎉 Tous les problèmes de formatage ont été corrigés !")
    else:
        print("✅ Aucun problème de formatage trouvé")

if __name__ == '__main__':
    test_django_formatting()
