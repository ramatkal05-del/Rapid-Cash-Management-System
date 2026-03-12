#!/usr/bin/env python
"""
Configuration Tailwind CSS pour production sans npm
Télécharge et configure Tailwind CSS en mode standalone
"""

import os
import urllib.request
import ssl

def setup_tailwind_production():
    """Configure Tailwind CSS pour production"""
    
    print("🎨 CONFIGURATION TAILWIND CSS PRODUCTION")
    print("=" * 50)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    css_dir = os.path.join(static_dir, 'css')
    
    # Créer les dossiers
    os.makedirs(css_dir, exist_ok=True)
    print(f"✅ Dossier créé: {css_dir}")
    
    # Télécharger Tailwind CSS standalone CLI
    tailwind_url = "https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.1/tailwindcss-windows-x64.exe"
    tailwind_path = os.path.join(base_dir, 'tailwindcss.exe')
    
    if not os.path.exists(tailwind_path):
        print(f"\n⬇️ Téléchargement de Tailwind CSS CLI...")
        try:
            # Créer un contexte SSL qui ignore les certificats (pour le téléchargement)
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            urllib.request.urlretrieve(tailwind_url, tailwind_path)
            print(f"✅ Tailwind CSS téléchargé")
        except Exception as e:
            print(f"⚠️ Erreur téléchargement: {e}")
            print(f"   Solution alternative: Utiliser le CDN avec intégrité")
            return False
    else:
        print(f"✅ Tailwind CSS CLI déjà présent")
    
    # Créer le fichier de configuration tailwind.config.js
    config_path = os.path.join(base_dir, 'tailwind.config.js')
    config_content = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './**/templates/**/*.html',
    './static/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#07080e',
          surface1: '#0d0e18',
          surface2: '#131421',
          surface3: '#1a1b2e',
          border: '#252640',
        },
        accent: {
          primary: '#4f8ef7',
          secondary: '#6b8cff',
          purple: '#8b5cf6',
          success: '#10b981',
          danger: '#ef4444',
          warning: '#f59e0b',
        },
        text: {
          main: '#e8eaf6',
          muted: '#64748b',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
"""
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    print(f"✅ tailwind.config.js créé")
    
    # Créer le fichier CSS source
    input_css_path = os.path.join(css_dir, 'input.css')
    css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom classes */
.card-dark {
    @apply bg-dark-surface1 border border-dark-border rounded-lg;
}

.btn-primary {
    @apply px-4 py-2 bg-accent-primary text-white rounded-lg hover:bg-accent-secondary transition-colors;
}

.btn-secondary {
    @apply px-4 py-2 bg-dark-surface2 text-text-main rounded-lg hover:bg-dark-surface3 transition-colors;
}

.input-dark {
    @apply w-full px-4 py-2 bg-dark-surface3 border border-dark-border rounded-lg text-text-main;
}
"""
    
    with open(input_css_path, 'w') as f:
        f.write(css_content)
    print(f"✅ input.css créé")
    
    # Créer le fichier CSS compilé (version de base si Tailwind CLI ne fonctionne pas)
    output_css_path = os.path.join(css_dir, 'tailwind.css')
    
    # Générer un CSS de base avec les classes essentielles
    essential_css = """/* Tailwind CSS Essential Classes */
*, ::before, ::after { box-sizing: border-box; border-width: 0; border-style: solid; border-color: #252640; }
html { line-height: 1.5; -webkit-text-size-adjust: 100%; }
body { margin: 0; line-height: inherit; background-color: #07080e; color: #e8eaf6; font-family: 'Inter', sans-serif; }

/* Layout */
.container { width: 100%; margin-left: auto; margin-right: auto; padding-left: 1rem; padding-right: 1rem; }
@media (min-width: 640px) { .container { max-width: 640px; } }
@media (min-width: 768px) { .container { max-width: 768px; } }
@media (min-width: 1024px) { .container { max-width: 1024px; } }
@media (min-width: 1280px) { .container { max-width: 1280px; } }

/* Grid */
.grid { display: grid; }
.grid-cols-1 { grid-template-columns: repeat(1, minmax(0, 1fr)); }
@media (min-width: 768px) { .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1024px) { .lg\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
.gap-4 { gap: 1rem; }
.gap-6 { gap: 1.5rem; }

/* Flex */
.flex { display: flex; }
.items-center { align-items: center; }
.justify-center { justify-content: center; }
.justify-between { justify-content: space-between; }
.justify-end { justify-content: flex-end; }
.gap-2 { gap: 0.5rem; }
.gap-3 { gap: 0.75rem; }
.gap-6 { gap: 1.5rem; }

/* Spacing */
.p-4 { padding: 1rem; }
.p-6 { padding: 1.5rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }
.px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
.m-0 { margin: 0; }
.mb-2 { margin-bottom: 0.5rem; }
.mb-4 { margin-bottom: 1rem; }
.mb-6 { margin-bottom: 1.5rem; }
.mr-2 { margin-right: 0.5rem; }
.mt-1 { margin-top: 0.25rem; }
.mt-2 { margin-top: 0.5rem; }
.mt-4 { margin-top: 1rem; }

/* Typography */
.text-sm { font-size: 0.875rem; line-height: 1.25rem; }
.text-lg { font-size: 1.125rem; line-height: 1.75rem; }
.text-2xl { font-size: 1.5rem; line-height: 2rem; }
.font-medium { font-weight: 500; }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }
.text-right { text-align: right; }

/* Colors - Background */
.bg-dark-bg { background-color: #07080e; }
.bg-dark-surface1 { background-color: #0d0e18; }
.bg-dark-surface2 { background-color: #131421; }
.bg-dark-surface3 { background-color: #1a1b2e; }
.bg-accent-primary { background-color: #4f8ef7; }
.bg-accent-success { background-color: #10b981; }
.bg-accent-danger { background-color: #ef4444; }

/* Colors - Text */
.text-text-main { color: #e8eaf6; }
.text-text-muted { color: #64748b; }
.text-white { color: #ffffff; }
.text-accent-success { color: #10b981; }
.text-accent-danger { color: #ef4444; }
.text-accent-primary { color: #4f8ef7; }

/* Borders */
.border { border-width: 1px; }
.border-dark-border { border-color: #252640; }
.rounded-lg { border-radius: 0.5rem; }
.rounded-full { border-radius: 9999px; }

/* Display */
.hidden { display: none; }
.block { display: block; }
.w-full { width: 100%; }
.w-4 { width: 1rem; }
.w-8 { width: 2rem; }
.w-10 { width: 2.5rem; }
.w-24 { width: 6rem; }
.h-4 { height: 1rem; }
.h-8 { height: 2rem; }
.h-10 { height: 2.5rem; }
.h-24 { height: 6rem; }
.max-w-4xl { max-width: 56rem; }
.flex-1 { flex: 1 1 0%; }

/* Effects */
.transition-colors { transition-property: color, background-color, border-color; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
.hover\\:bg-accent-secondary:hover { background-color: #6b8cff; }
.hover\\:bg-dark-surface3:hover { background-color: #1a1b2e; }

/* Custom Components */
.card-dark { background-color: #0d0e18; border: 1px solid #252640; border-radius: 0.5rem; }
.btn-primary { padding: 0.5rem 1rem; background-color: #4f8ef7; color: white; border-radius: 0.5rem; }
.btn-secondary { padding: 0.5rem 1rem; background-color: #131421; color: #e8eaf6; border-radius: 0.5rem; }
.input-dark { width: 100%; padding: 0.75rem 1rem; background-color: #1a1b2e; border: 1px solid #252640; border-radius: 0.5rem; color: #e8eaf6; }
"""
    
    with open(output_css_path, 'w') as f:
        f.write(essential_css)
    print(f"✅ tailwind.css créé (version essentielle)")
    
    print(f"\n📋 PROCHAINES ÉTAPES:")
    print(f"   1. Redémarrer le serveur Django")
    print(f"   2. Modifier base.html pour utiliser: {{% static 'css/tailwind.css' %}}")
    print(f"   3. Au lieu du CDN actuel")
    print(f"\n💡 Alternative: Continuer avec le CDN (plus simple pour le dev)")
    print(f"   Le warning est normal en développement.")
    
    return True

if __name__ == '__main__':
    setup_tailwind_production()
