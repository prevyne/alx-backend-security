# ip_tracking/middleware.py
import requests
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
        self.blocked_ips = set(BlockedIP.objects.values_list('ip_address', flat=True))

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip in self.blocked_ips:
            return HttpResponseForbidden("Your IP address has been blocked.")

        if ip:
            # Geolocation lookup with caching
            cache_key = f"geolocation_{ip}"
            geo_data = cache.get(cache_key)

            if not geo_data:
                try:
                    # Using a free geolocation API
                    response = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
                    response.raise_for_status()
                    data = response.json()
                    geo_data = {
                        'country': data.get('country'),
                        'city': data.get('city'),
                    }
                    # Cache for 24 hours
                    cache.set(cache_key, geo_data, 60 * 60 * 24) 
                except requests.RequestException:
                    geo_data = {'country': None, 'city': None}

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=geo_data.get('country'),
                city=geo_data.get('city')
            )

        response = self.get_response(request)
        return response