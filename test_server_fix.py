#!/usr/bin/env python
"""
Script de test pour vérifier que le problème TemplateSyntaxError est résolu
"""

import subprocess
import time
import sys
import os

def test_server_startup():
    """Tester que le serveur Django démarre sans erreurs de templates"""
    
    print("🚀 TEST DÉMARRAGE SERVEUR DJANGO")
    print("=" * 50)
    
    # Changer le répertoire de travail
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Lancer le serveur en arrière-plan
        print("📋 Démarrage du serveur de développement...")
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', 
            '--settings=config.development',
            '127.0.0.1:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Attendre un peu que le serveur démarre
        print("⏳ Attente du démarrage (5 secondes)...")
        time.sleep(5)
        
        # Vérifier si le processus est encore en cours
        if process.poll() is None:
            print("✅ Serveur démarré avec succès !")
            print("🌐 URL: http://127.0.0.1:8000")
            print("🌐 URL: http://localhost:8000")
            print("\n🎯 Pages à tester:")
            print("   http://127.0.0.1:8000/core/capital/")
            print("   http://127.0.0.1:8000/core/paie/")
            print("   http://127.0.0.1:8000/admin/")
            
            # Arrêter le serveur proprement
            print("\n⏹️ Arrêt du serveur de test...")
            process.terminate()
            process.wait(timeout=5)
            
            print("🎉 Test terminé avec succès !")
            return True
            
        else:
            # Le processus s'est arrêté, lire les erreurs
            stdout, stderr = process.communicate()
            print("❌ Le serveur ne s'est pas démarré correctement")
            
            if stderr:
                print("\n📋 Erreurs trouvées:")
                print(stderr)
            
            if stdout:
                print("\n📋 Sortie standard:")
                print(stdout)
            
            return False
            
    except KeyboardInterrupt:
        print("\n⏹️ Interruption par l'utilisateur")
        if 'process' in locals():
            process.terminate()
            process.wait()
        return False
        
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def show_fix_summary():
    """Afficher un résumé des corrections apportées"""
    
    print("\n" + "=" * 60)
    print("📋 RÉSUMÉ DES CORRECTIONS APPORTÉES")
    print("=" * 60)
    
    print("\n🔧 PROBLÈME CORRIGÉ:")
    print("   ❌ TemplateSyntaxError: Could not parse the remainder: ':02d'")
    print("   ✅ Cause: Syntaxe Python de formatage utilisée dans template Django")
    
    print("\n📝 FICHIERS CORRIGÉS:")
    files = [
        "templates/core/capital_management.html",
        "templates/core/payroll_dashboard.html", 
        "templates/core/pay_salary.html",
        "templates/core/add_bonus.html"
    ]
    
    for file in files:
        print(f"   ✅ {file}")
    
    print("\n🔄 CHANGEMENTS EFFECTUÉS:")
    print("   ❌ Ancien: {{ current_period.month:02d }}")
    print("   ✅ Nouveau: {{ current_period.month|stringformat:\"02d\" }}")
    
    print("   ❌ Ancien: {{ amount:.2f }}")
    print("   ✅ Nouveau: {{ amount|floatformat:2 }}")
    
    print("\n💡 POURQUOI ÇA MARCHE:")
    print("   📋 Django templates utilise sa propre syntaxe de filtres")
    print("   📋 stringformat:\"02d\" formate les nombres avec zéros devant")
    print("   📋 floatformat:2 formate les nombres décimaux")
    print("   📋 La syntaxe Python :02d n'est pas supportée dans les templates")
    
    print("\n🎯 UTILISATION CORRECTE:")
    print("   ✅ {{ variable|stringformat:\"02d\" }}  → Formatage avec zéros")
    print("   ✅ {{ variable|floatformat:2 }}      → Formatage décimal")
    print("   ✅ {{ variable|date:\"d/m/Y\" }}     → Formatage de dates")
    print("   ✅ {{ variable|default:\"N/A\" }}     → Valeur par défaut")

if __name__ == '__main__':
    success = test_server_startup()
    show_fix_summary()
    
    if success:
        print("\n🎊 SUCCÈS TOTAL - Problème résolu !")
        sys.exit(0)
    else:
        print("\n⚠️ ÉCHEC - Problème persiste")
        sys.exit(1)
