from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from ipware import get_client_ip

class IPLoggingMiddleware:
    """
    Middleware that logs requests and blocks IPs found in the BlockedIP list.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Cache the set of blocked IPs for faster lookups
        self.blocked_ips = set(BlockedIP.objects.values_list('ip_address', flat=True))


    def __call__(self, request):
        ip, _ = get_client_ip(request)

        # Check if the IP is in our cached blacklist
        if ip in self.blocked_ips:
            return HttpResponseForbidden("Your IP address has been blocked.")

        if ip:
            RequestLog.objects.create(
                ip_address=ip,
                path=request.path
            )

        response = self.get_response(request)
        return response