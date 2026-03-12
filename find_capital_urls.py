#!/usr/bin/env python
"""
Rechercher les URLs capital_management dans les templates
"""

import os

def find_capital_management_urls():
    """Trouver où capital_management est utilisé dans les templates"""
    
    print("🔍 RECHERCHE URL capital_management DANS LES TEMPLATES")
    print("=" * 60)
    
    template_dir = 'templates'
    found_files = []
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'capital_management' in content:
                        found_files.append(file_path)
                        
                        # Trouver les lignes contenant capital_management
                        lines = content.split('\n')
                        for i, line in enumerate(lines, 1):
                            if 'capital_management' in line:
                                print(f"   📄 {file_path}:{i}")
                                print(f"      {line.strip()}")
                        
                except Exception as e:
                    print(f"   ❌ Erreur lecture {file_path}: {e}")
    
    if found_files:
        print(f"\n🎯 TROUVÉ DANS {len(found_files)} FICHIER(S):")
        for file in found_files:
            print(f"   📄 {file}")
    else:
        print("\n✅ Aucune utilisation de 'capital_management' trouvée")
    
    print("\n💡 PROBLÈME POSSIBLE:")
    print("   Si 'capital_management' est utilisé sans namespace:")
    print("   ❌ {% url 'capital_management' %}  # Incorrect")
    print("   ✅ {% url 'core:capital_management' %}  # Correct")
    
    print("\n🔧 SOLUTION:")
    print("   1. Ajouter le namespace 'core:' aux URLs")
    print("   2. Ou utiliser les URLs complètes")
    print("   3. Vérifier toutes les références d'URL")

if __name__ == '__main__':
    find_capital_management_urls()
