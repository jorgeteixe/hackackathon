from django.core.management.base import BaseCommand
from django.core.mail import mail_admins


class Command(BaseCommand):
    def handle(self, *args, **options):
        mail_admins("Test desde Django", "Django los envía?", fail_silently=False)
