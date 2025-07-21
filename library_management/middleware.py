from django.http import HttpResponseForbidden
from django.conf import settings
import re
import urllib.parse
from urllib.parse import unquote

def is_suspicious_request(self, request):
    # Decode full path (so %3Cscript%3E becomes <script>)
    decoded_path = urllib.parse.unquote(request.get_full_path())

    suspicious_patterns = [
        r'<script[^>]*>.*?</script>',
        r'javascript:',
        r'union.*select',
        r'drop.*table',
    ]

    # Check URL (decoded)
    for pattern in suspicious_patterns:
        if re.search(pattern, decoded_path, re.IGNORECASE):
            return True

    # Check POST data
    if hasattr(request, 'POST'):
        for value in request.POST.values():
            if re.search(pattern, str(value), re.IGNORECASE):
                return True

    return False

# class SecurityMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
    
#     def __call__(self, request):
#         # Check for suspicious patterns in request
#         if self.is_suspicious_request(request):
#             return HttpResponseForbidden("Suspicious request detected")
        
#         response = self.get_response(request)
        
#         # Add security headers
#         response['X-Content-Type-Options'] = 'nosniff'
#         response['X-Frame-Options'] = 'DENY'
#         response['X-XSS-Protection'] = '1; mode=block'
#         response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
#         return response
    
#     def is_suspicious_request(self, request):
#         # Check for common attack patterns
#         suspicious_patterns = [
#             r'<script[^>]*>.*?</script>',
#             r'javascript:',
#             r'union.*select',
#             r'drop.*table',
#         ]
        
#         for pattern in suspicious_patterns:
#             if re.search(pattern, request.get_full_path(), re.IGNORECASE):
#                 return True
            
#             # Check POST data
#             if hasattr(request, 'POST'):
#                 for value in request.POST.values():
#                     if re.search(pattern, str(value), re.IGNORECASE):
#                         return True
        
#         return False

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Decode full URL (query + path) so encoded payloads like %3Cscript%3E get caught
        full_path = unquote(request.get_full_path())

        # Check for suspicious patterns BEFORE Django resolves URLs
        suspicious_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'union.*select',
            r'drop.*table',
        ]
        for pattern in suspicious_patterns:
            if re.search(pattern, full_path, re.IGNORECASE):
                return HttpResponseForbidden("Suspicious request detected")

            # Check POST data (if present)
            if hasattr(request, "POST"):
                for value in request.POST.values():
                    if re.search(pattern, str(value), re.IGNORECASE):
                        return HttpResponseForbidden("Suspicious request detected")

        # Continue with normal processing
        response = self.get_response(request)

        # Add security headers to *all* responses
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"
        response["X-XSS-Protection"] = "1; mode=block"
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        return response
