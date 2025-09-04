from celery import shared_task
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_suspicious_ips():
    """
    A Celery task to detect and flag suspicious IPs based on request patterns.
    This task should be scheduled to run periodically (e.g., hourly).
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # 1. Find IPs with more than 100 requests in the last hour
    high_volume_ips = RequestLog.objects.filter(timestamp__gte=one_hour_ago) \
        .values('ip_address') \
        .annotate(request_count=Count('id')) \
        .filter(request_count__gt=100)

    for item in high_volume_ips:
        SuspiciousIP.objects.update_or_create(
            ip_address=item['ip_address'],
            defaults={'reason': f"High request volume: {item['request_count']} requests in the last hour."}
        )

    # 2. Find IPs accessing sensitive paths
    sensitive_paths = ['/admin/', '/login/']
    sensitive_access_ips = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values_list('ip_address', flat=True).distinct()

    for ip in sensitive_access_ips:
        SuspiciousIP.objects.update_or_create(
            ip_address=ip,
            defaults={'reason': 'Accessed sensitive paths like /admin or /login.'}
        )

    return f"Checked {high_volume_ips.count()} high-volume IPs and {len(sensitive_access_ips)} sensitive-access IPs."