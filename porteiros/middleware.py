# porteiros/middleware.py

from django.utils.timezone import now

class RegistrarLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
      
        response = self.get_response(request)
      
        return response
