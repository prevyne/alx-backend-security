from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

def get_rate_limit(group, request):
    """
    Dynamically determine the rate limit based on authentication status.
    """
    if request.user.is_authenticated:
        return '10/m'  # 10 requests per minute for authenticated users
    return '5/m'   # 5 requests per minute for anonymous users

@ratelimit(key='ip', rate=get_rate_limit, method='GET', block=True)
def sensitive_view(request):
    """
    A view protected by dynamic rate limiting.
    """
    return HttpResponse("This is a rate-limited view. You can access it.")

def test_api_view(request):
    # This view will trigger the IP tracking middleware
    return HttpResponse("API test page is working. Your visit has been logged.")