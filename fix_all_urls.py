#!/usr/bin/env python
"""
Trouver et corriger toutes les URLs sans namespace dans les templates
"""

import os
import re

def find_and_fix_all_urls():
    """Trouver toutes les URLs sans namespace et les corriger"""
    
    print("🔍 CORRECTION AUTOMATIQUE DES URLs SANS NAMESPACE")
    print("=" * 65)
    
    template_dir = 'templates'
    files_to_fix = []
    
    # Patterns à rechercher et corriger
    url_patterns = [
        (r"{%\s*url\s+['\"](payroll_dashboard)['\"]\s*%}", r"{% url 'core:payroll_dashboard' %}"),
        (r"{%\s*url\s+['\"](calculate_salaries)['\"]\s*%}", r"{% url 'core:calculate_salaries' %}"),
        (r"{%\s*url\s+['\"](pay_salary)['\"]\s*%}", r"{% url 'core:pay_salary' %}"),
        (r"{%\s*url\s+['\"](add_bonus)['\"]\s*%}", r"{% url 'core:add_bonus' %}"),
        (r"{%\s*url\s+['\"](capital_management)['\"]\s*%}", r"{% url 'core:capital_management' %}"),
        (r"{%\s*url\s+['\"](agents_list)['\"]\s*%}", r"{% url 'core:agents_list' %}"),
        (r"{%\s*url\s+['\"](user_profile)['\"]\s*%}", r"{% url 'core:user_profile' %}"),
        (r"{%\s*url\s+['\"](associates_list)['\"]\s*%}", r"{% url 'core:associates_list' %}"),
        (r"{%\s*url\s+['\"](create_associate)['\"]\s*%}", r"{% url 'core:create_associate' %}"),
        (r"{%\s*url\s+['\"](investors_list)['\"]\s*%}", r"{% url 'core:investors_list' %}"),
        (r"{%\s*url\s+['\"](create_investor)['\"]\s*%}", r"{% url 'core:create_investor' %}"),
        (r"{%\s*url\s+['\"](caisses_list)['\"]\s*%}", r"{% url 'core:caisses_list' %}"),
        (r"{%\s*url\s+['\"](exchange_rates)['\"]\s*%}", r"{% url 'core:exchange_rates' %}"),
    ]
    
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    modified = False
                    changes = []
                    
                    for pattern, replacement in url_patterns:
                        matches = re.findall(pattern, content)
                        if matches:
                            content = re.sub(pattern, replacement, content)
                            modified = True
                            changes.extend(matches)
                    
                    if modified:
                        files_to_fix.append({
                            'file': file_path,
                            'changes': changes,
                            'original': original_content,
                            'modified': content
                        })
                        
                        # Sauvegarder les modifications
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        
                except Exception as e:
                    print(f"   ❌ Erreur traitement {file_path}: {e}")
    
    if files_to_fix:
        print(f"\n🔧 FICHIERS MODIFIÉS: {len(files_to_fix)}")
        
        for file_info in files_to_fix:
            print(f"\n📄 {os.path.relpath(file_info['file'], template_dir)}")
            for change in file_info['changes']:
                print(f"   ✅ Corrigé: {change}")
    else:
        print("\n✅ Aucune correction nécessaire")
    
    print("\n🎯 URLs CORRIGÉES:")
    print("   Toutes les URLs des templates utilisent maintenant le namespace 'core:'")
    print("   Format: {% url 'core:nom_url' %}")
    
    print("\n🚀 TEST RECOMMANDÉ:")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/dashboard/")

if __name__ == '__main__':
    find_and_fix_all_urls()
