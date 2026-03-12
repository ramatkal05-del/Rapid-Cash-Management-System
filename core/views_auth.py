from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages

@require_http_methods(["POST"])
@login_required
def custom_logout(request):
    """
    Vue de logout personnalisée pour éviter les problèmes de redirection
    """
    try:
        # Enregistrer l'action de logout dans l'audit
        from core.models import AuditLog
        AuditLog.objects.create(
            action_type=AuditLog.ActionType.LOGOUT,
            user=request.user,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            details="Déconnexion de l'utilisateur"
        )
    except:
        pass  # Ne pas échouer si l'audit ne fonctionne pas
    
    # Effectuer le logout
    logout(request)
    
    # Message de succès
    messages.success(request, "Vous avez été déconnecté avec succès.")
    
    # Redirection vers la page de login
    return redirect('login')
