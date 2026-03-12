from django.utils.deprecation import MiddlewareMixin

class UTF8Middleware(MiddlewareMixin):
    """
    Middleware pour garantir l'encodage UTF-8 dans toutes les requêtes/réponses
    """
    
    def process_request(self, request):
        """S'assurer que la requête utilise UTF-8"""
        if hasattr(request, 'encoding') and request.encoding != 'utf-8':
            request.encoding = 'utf-8'
        return None
    
    def process_response(self, request, response):
        """S'assurer que la réponse utilise UTF-8"""
        if 'Content-Type' in response and 'charset' not in response['Content-Type']:
            response['Content-Type'] = f"{response['Content-Type']}; charset=utf-8"
        
        # Ajouter des headers UTF-8 supplémentaires
        response['Content-Language'] = 'fr'
        return response
