from django.db import models

class RequestLog(models.Model):
    """
    Model to store details of incoming requests.
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.ip_address} at {self.timestamp} on {self.path}"
    
class BlockedIP(models.Model):
    """
    Model to store IP addresses that are blocked from accessing the site.
    """
    ip_address = models.GenericIPAddressField(unique=True)

    def __str__(self):
        return self.ip_address