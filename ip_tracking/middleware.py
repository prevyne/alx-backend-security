from django.core.cache import cache
from django.http import HttpResponseForbidden
from .models import RequestLog, BlockedIP
from ipware import get_client_ip

class IPLoggingMiddleware:
    """
    Middleware that logs requests, blocks IPs, and adds geolocation data.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # It's better to fetch this from the DB or a cache that can be updated
        self.blocked_ips = set(BlockedIP.objects.values_list('ip_address', flat=True))

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip in self.blocked_ips:
            return HttpResponseForbidden("Your IP address has been blocked.")

        if ip:
            country = None
            city = None

            # Check if geolocation data is available from the ip_geolocation middleware
            if hasattr(request, 'ip_geolocation_info'):
                geo_info = request.ip_geolocation_info
                country = geo_info.get('country')
                city = geo_info.get('city')

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city
            )

        response = self.get_response(request)
        return response