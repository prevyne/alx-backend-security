from django.contrib import admin
from .models import RequestLog, BlockedIP, SuspiciousIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'timestamp', 'country', 'city')
    list_filter = ('timestamp', 'country')
    search_fields = ('ip_address', 'path')
    readonly_fields = ('ip_address', 'timestamp', 'path', 'country', 'city')

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)
    search_fields = ('ip_address',)

@admin.register(SuspiciousIP)
class SuspiciousIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'reason', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('ip_address', 'reason')
    readonly_fields = ('ip_address', 'reason', 'timestamp')