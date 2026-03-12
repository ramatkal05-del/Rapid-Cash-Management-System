#!/usr/bin/env python
"""
Diagnostic rapide du problème HTTP/HTTPS
"""

def quick_diagnose():
    """Diagnostic rapide et solutions immédiates"""
    
    print("🔍 DIAGNOSTIC RAPIDE HTTP/HTTPS")
    print("=" * 40)
    
    print("\n🎯 CAUSE PROBABLE:")
    print("   Extension navigateur ou cache HSTS force HTTPS")
    
    print("\n💡 SOLUTIONS RAPIDES:")
    print("   1. http://localhost:8000 (utiliser http://)")
    print("   2. Mode navigation privée")
    print("   3. Désactiver extensions HTTPS")
    print("   4. Vider cache navigateur")
    
    print("\n🚀 LANCEMENT RECOMMANDÉ:")
    print("   python run_dev.py")
    print("   ou")
    print("   python manage.py runserver --settings=config.development")
    
    print("\n⚠️  À FAIRE:")
    print("   - Toujours utiliser http:// en local")
    print("   - Pas https:// pour development server")
    print("   - Mode privé si problème persiste")
    
    print("\n" + "=" * 40)

if __name__ == '__main__':
    quick_diagnose()
