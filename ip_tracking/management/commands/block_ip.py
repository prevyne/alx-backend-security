from django.core.management.base import BaseCommand
from ip_tracking.models import BlockedIP

class Command(BaseCommand):
    help = 'Adds an IP address to the blacklist.'

    def add_arguments(self, parser):
        parser.add_argument('ip_address', type=str, help='The IP address to block.')

    def handle(self, *args, **options):
        ip_address = options['ip_address']
        obj, created = BlockedIP.objects.get_or_create(ip_address=ip_address)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully blocked IP: {ip_address}'))
        else:
            self.stdout.write(self.style.WARNING(f'IP address {ip_address} was already blocked.'))