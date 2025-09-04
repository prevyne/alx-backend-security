from django.db import models

class RequestLog(models.Model):
    """
    Model to store details of incoming requests, including geolocation.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        location = f"{self.city}, {self.country}" if self.city and self.country else "Unknown Location"
        return f"{self.ip_address} from {location} at {self.timestamp}"
    
class BlockedIP(models.Model):
    """
    Model to store IP addresses that are blocked from accessing the site.
    """
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address

class SuspiciousIP(models.Model):
    """
    Model to store IPs flagged for suspicious activity.
    """
    ip_address = models.GenericIPAddressField(unique=True)
    reason = models.TextField(help_text="Reason for flagging the IP as suspicious.")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} flagged for {self.reason}"
