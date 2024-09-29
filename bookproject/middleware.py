# middleware.py
from django.http import HttpResponseForbidden

class BlockIPMiddleware:
    # List of blocked IPs
    BLOCKED_IPS = ['152.58.90.14', '203.0.113.5']
    
    # List of allowed IPs (if you are whitelisting)
    ALLOWED_IPS = ['192.168.1.100', '203.0.113.20']

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = self.get_client_ip(request)

        # Check if the IP is blocked (blacklist mode)
        if ip in self.BLOCKED_IPS:
            return HttpResponseForbidden("<h1>Access Denied: Your IP is blocked.</h1>")

        # If using whitelist mode, block all IPs not in ALLOWED_IPS
        # Uncomment this block if you want to allow only specific IPs
        # if ip not in self.ALLOWED_IPS:
        #     return HttpResponseForbidden("<h1>Access Denied: Your IP is not allowed.</h1>")

        # Continue processing request if IP is allowed
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        # Extract the client's IP from the request headers
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
