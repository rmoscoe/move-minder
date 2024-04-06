from django.utils.deprecation import MiddlewareMixin

class FrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'sameorigin'
        return response