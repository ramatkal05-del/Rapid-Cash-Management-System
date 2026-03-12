from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles):
    """
    Decorator for views that checks that the user has a specific role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            
            if request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, "Vous n'avez pas les permissions nécessaires pour accéder à cette page.")
            return redirect('dashboard')
        return _wrapped_view
    return decorator

def admin_required(view_func):
    """Shortcut for ADMIN role requirement."""
    return role_required(['ADMIN'])(view_func)

def agent_required(view_func):
    """Shortcut for AGENT role requirement."""
    return role_required(['AGENT'])(view_func)
