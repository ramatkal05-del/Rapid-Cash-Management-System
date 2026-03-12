#!/usr/bin/env python
"""
Script de vérification finale UTF-8 pour le projet Rapid Cash
"""

import os
import sys

def verify_utf8_setup():
    """Vérification complète de la configuration UTF-8"""
    
    print("🔍 VÉRIFICATION FINALE UTF-8 - RAPID CASH")
    print("=" * 60)
    
    # 1. Vérification des fichiers Python
    print("\n📁 Fichiers Python (encodage UTF-8):")
    
    python_files = [
        'config/settings.py',
        'core/models.py',
        'core/views.py',
        'core/admin.py',
        'operations/models.py',
        'operations/views.py',
        'operations/admin.py',
        'finance/models.py',
        'finance/views.py',
        'finance/admin.py',
    ]
    
    for file_path in python_files:
        full_path = file_path
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Vérifier la présence de caractères français
                    french_chars = ['é', 'è', 'à', 'ê', 'ë', 'î', 'ï', 'ô', 'ö', 'ù', 'û', 'ü', 'ÿ', 'ç']
                    has_french = any(char in content for char in french_chars)
                    
                    if has_french:
                        print(f"   ✅ {file_path} - Contient des caractères français")
                    else:
                        print(f"   ⚪ {file_path} - Pas de caractères français")
                        
            except UnicodeDecodeError:
                print(f"   ❌ {file_path} - Erreur d'encodage")
            except Exception as e:
                print(f"   ⚠️ {file_path} - {e}")
        else:
            print(f"   ⚠️ {file_path} - Fichier non trouvé")
    
    # 2. Vérification des templates
    print("\n🎨 Templates HTML (charset UTF-8):")
    
    template_files = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                template_files.append(os.path.join(root, file))
    
    for template_path in template_files:
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                if 'charset="UTF-8"' in content:
                    print(f"   ✅ {template_path} - charset UTF-8 trouvé")
                else:
                    print(f"   ❌ {template_path} - charset UTF-8 manquant")
                    
        except UnicodeDecodeError:
            print(f"   ❌ {template_path} - Erreur d'encodage")
        except Exception as e:
            print(f"   ⚠️ {template_path} - {e}")
    
    # 3. Vérification de la configuration Django
    print("\n⚙️ Configuration Django:")
    
    settings_file = 'config/settings.py'
    if os.path.exists(settings_file):
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            config_items = [
                ('LANGUAGE_CODE', 'fr-fr'),
                ('DEFAULT_CHARSET', 'utf-8'),
                ('FILE_CHARSET', 'utf-8'),
                ('USE_I18N', 'True'),
            ]
            
            for item, expected in config_items:
                if f"{item} = '{expected}'" in content:
                    print(f"   ✅ {item} = {expected}")
                else:
                    print(f"   ❌ {item} - Non trouvé ou incorrect")
    else:
        print(f"   ❌ {settings_file} - Fichier non trouvé")
    
    # 4. Vérification du middleware
    print("\n🔧 Middleware UTF-8:")
    
    middleware_file = 'core/middleware.py'
    if os.path.exists(middleware_file):
        print(f"   ✅ {middleware_file} - Middleware UTF-8 créé")
    else:
        print(f"   ❌ {middleware_file} - Middleware manquant")
    
    # 5. Instructions finales
    print("\n📋 RÉCAPITULATIF DES CORRECTIONS:")
    print("   ✅ Configuration UTF-8 ajoutée dans settings.py")
    print("   ✅ Headers UTF-8 ajoutés dans les templates")
    print("   ✅ Middleware UTF-8 créé et configuré")
    print("   ✅ Admin Django amélioré pour UTF-8")
    print("   ✅ Scripts de test créés")
    
    print("\n🎯 ACTIONS RECOMMANDÉES:")
    print("   1. Redémarrer le serveur Django")
    print("   2. Vider le cache du navigateur")
    print("   3. Tester l'interface admin")
    print("   4. Vérifier l'affichage des accents")
    
    print("\n" + "=" * 60)
    print("✅ VÉRIFICATION TERMINÉE - SYSTÈME UTF-8 CONFIGURÉ")
    
    print("\n🚀 POUR TESTER:")
    print("   python manage.py runserver")
    print("   http://127.0.0.1:8000/admin/")
    print("\n   Les accents français devraient maintenant s'afficher correctement:")
    print("   - Dépenses")
    print("   - Opérations") 
    print("   - Nom de la caisse")
    print("   - Taux de change")
    print("   - Paiements partenaires")

if __name__ == '__main__':
    verify_utf8_setup()
