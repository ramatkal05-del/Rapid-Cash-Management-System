#!/usr/bin/env python
"""
Diagnostic du POST /core/profil/ 500 Internal Server Error
"""

import os

def diagnose_profile_500():
    """Diagnostiquer l'erreur 500 sur le profil"""
    
    print("🔍 DIAGNOSTIC POST /core/profil/ 500")
    print("=" * 50)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    try:
        import django
        django.setup()
        
        from django.contrib.auth import get_user_model
        from core.forms import UserProfileForm
        from django.core.files.uploadedfile import SimpleUploadedFile
        import io
        
        User = get_user_model()
        
        print("\n👤 TEST UTILISATEUR:")
        user = User.objects.first()
        if not user:
            print("❌ Aucun utilisateur trouvé")
            return
        
        print(f"   Utilisateur: {user.username}")
        print(f"   Email: {user.email}")
        
        print("\n📝 TEST FORMULAIRE UserProfileForm:")
        
        # Test 1: Formulaire vide (GET simulation)
        form_get = UserProfileForm(instance=user)
        print(f"   ✅ GET /core/profil/ - Formulaire initialisé")
        
        # Test 2: Formulaire POST avec données valides
        post_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': user.email or 'test@test.com',
            'phone': '1234567890'
        }
        
        form_post = UserProfileForm(post_data, instance=user)
        if form_post.is_valid():
            print(f"   ✅ POST avec données valides - Formulaire valide")
            
            # Essayer de sauvegarder
            try:
                form_post.save()
                print(f"   ✅ Sauvegarde réussie")
            except Exception as e:
                print(f"   ❌ Erreur sauvegarde: {e}")
        else:
            print(f"   ❌ Formulaire invalide:")
            for field, errors in form_post.errors.items():
                print(f"      {field}: {errors}")
        
        # Test 3: Vérifier les champs du modèle User
        print(f"\n🔧 VÉRIFICATION CHAMPS USER:")
        user_fields = [f.name for f in User._meta.fields]
        required_fields = ['first_name', 'last_name', 'email', 'phone', 'profile_picture']
        
        for field in required_fields:
            if field in user_fields:
                print(f"   ✅ {field}: présent")
            else:
                print(f"   ❌ {field}: MANQUANT")
        
        # Test 4: Simuler POST avec fichier (profile_picture)
        print(f"\n📸 TEST UPLOAD PHOTO:")
        try:
            # Créer un faux fichier image
            fake_image = io.BytesIO(b'fake image content')
            fake_file = SimpleUploadedFile("test.jpg", fake_image.read(), content_type="image/jpeg")
            
            post_data_with_file = {
                'first_name': 'Test',
                'last_name': 'Photo',
                'email': user.email or 'photo@test.com',
                'phone': '0987654321'
            }
            
            form_file = UserProfileForm(post_data_with_file, {'profile_picture': fake_file}, instance=user)
            if form_file.is_valid():
                print(f"   ✅ Formulaire avec fichier valide")
            else:
                print(f"   ⚠️ Formulaire avec fichier invalide: {form_file.errors}")
        except Exception as e:
            print(f"   ⚠️ Erreur upload: {e}")
        
        print(f"\n📊 RÉSULTAT:")
        print(f"   Si tous les tests passent, le problème vient probablement:")
        print(f"   - De la vue (user_profile)")
        print(f"   - Du template (user_profile.html)")
        print(f"   - Ou d'une exception non gérée")
        
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    diagnose_profile_500()
