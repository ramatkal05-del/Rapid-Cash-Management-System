#!/usr/bin/env python
"""
Script de diagnostic HTTP/HTTPS pour Django Development Server
"""

import os
import sys
import socket
import urllib.request
import ssl

def diagnose_http_https_issue():
    """Diagnostic complet du problème HTTP/HTTPS"""
    
    print("🔍 DIAGNOSTIC HTTP/HTTPS - DJANGO DEVELOPMENT SERVER")
    print("=" * 60)
    
    # 1. Vérifier la configuration Django
    print("\n📋 Configuration Django:")
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
        import django
        django.setup()
        
        from django.conf import settings
        
        print(f"   DEBUG: {settings.DEBUG}")
        print(f"   ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        print(f"   SECURE_SSL_REDIRECT: {getattr(settings, 'SECURE_SSL_REDIRECT', 'Non défini')}")
        print(f"   SESSION_COOKIE_SECURE: {getattr(settings, 'SESSION_COOKIE_SECURE', 'Non défini')}")
        print(f"   CSRF_COOKIE_SECURE: {getattr(settings, 'CSRF_COOKIE_SECURE', 'Non défini')}")
        print(f"   SECURE_PROXY_SSL_HEADER: {getattr(settings, 'SECURE_PROXY_SSL_HEADER', 'Non défini')}")
        
    except Exception as e:
        print(f"   ❌ Erreur configuration Django: {e}")
    
    # 2. Tester les ports locaux
    print("\n🌐 Test des ports locaux:")
    
    def test_port(host, port, protocol):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                print(f"   ✅ {protocol}://{host}:{port} - Ouvert")
                return True
            else:
                print(f"   ❌ {protocol}://{host}:{port} - Fermé")
                return False
        except Exception as e:
            print(f"   ⚠️ {protocol}://{host}:{port} - Erreur: {e}")
            return False
    
    # Test des ports
    http_localhost = test_port('localhost', 8000, 'http')
    https_localhost = test_port('localhost', 8000, 'https')
    http_127 = test_port('127.0.0.1', 8000, 'http')
    https_127 = test_port('127.0.0.1', 8000, 'https')
    
    # 3. Tester les requêtes HTTP/HTTPS
    print("\n📡 Test des requêtes:")
    
    def test_request(url):
        try:
            context = ssl._create_unverified_context() if url.startswith('https') else None
            req = urllib.request.Request(url)
            
            with urllib.request.urlopen(req, timeout=5, context=context) as response:
                status = response.getcode()
                headers = dict(response.headers)
                
                print(f"   ✅ {url} - Status: {status}")
                print(f"      Server: {headers.get('Server', 'Inconnu')}")
                print(f"      Content-Type: {headers.get('Content-Type', 'Inconnu')}")
                return True
                
        except urllib.error.HTTPError as e:
            print(f"   ❌ {url} - HTTP Error: {e.code}")
            return False
        except urllib.error.URLError as e:
            print(f"   ❌ {url} - URL Error: {e.reason}")
            return False
        except Exception as e:
            print(f"   ❌ {url} - Erreur: {e}")
            return False
    
    # Test seulement si le serveur est probablement en cours d'exécution
    if http_localhost or http_127:
        test_request('http://localhost:8000')
        test_request('http://127.0.0.1:8000')
    
    # 4. Vérifier les proxies système
    print("\n🔧 Configuration Proxy:")
    
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
    
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"   ⚠️ {var}: {value}")
    
    if not any(os.environ.get(var) for var in proxy_vars):
        print("   ✅ Aucun proxy détecté")
    
    # 5. Vérifier les extensions navigateur possibles
    print("\n🌍 Causes possibles de redirection HTTPS:")
    
    causes = [
        "🔗 Extension navigateur 'HTTPS Everywhere' ou similaire",
        "🔗 Extension 'Force HTTPS' activée",
        "🔗 Paramètres du navigateur forçant HTTPS",
        "🔗 Antivirus/Firewall avec inspection SSL",
        "🔗 Proxy d'entreprise forçant HTTPS",
        "🔗 HSTS (HTTP Strict Transport Security) dans le cache navigateur",
        "🔗 Bookmark/suggestion en https://",
        "🔗 Historique de navigation avec HTTPS",
        "🔗 Configuration réseau locale",
    ]
    
    for cause in causes:
        print(f"   {cause}")
    
    # 6. Solutions recommandées
    print("\n💡 SOLUTIONS RECOMMANDÉES:")
    
    solutions = [
        "1. Utiliser http://localhost:8000 ou http://127.0.0.1:8000 explicitement",
        "2. Vider le cache du navigateur et les cookies pour localhost",
        "3. Désactiver temporairement les extensions de sécurité HTTPS",
        "4. Utiliser un navigateur en mode privé/incognito",
        "5. Vérifier les paramètres proxy système",
        "6. Redémarrer le serveur Django avec: python manage.py runserver",
    ]
    
    for solution in solutions:
        print(f"   {solution}")
    
    print("\n" + "=" * 60)
    print("🎯 DIAGNOSTIC TERMINÉ")

if __name__ == '__main__':
    diagnose_http_https_issue()
