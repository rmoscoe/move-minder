from django.http import HttpResponseForbidden
import os

class AuthenticationHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method != 'GET':
            header_value = request.headers.get("Authentication", None)
            if not request.path.startswith('/admin/login/'):
                if header_value is None or header_value != os.environ.get('AUTHENTICATION'):
                    return HttpResponseForbidden("Access denied")
        
        response = self.get_response(request)
        return response