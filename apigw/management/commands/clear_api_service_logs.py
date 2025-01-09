from django.core.management.base import BaseCommand
import datetime
from apigw import models


class Command(BaseCommand):
    help = "Remove old logs."

    def handle(self, *args, **options):
        days_for_deletion = datetime.datetime.now() - datetime.timedelta(days=20)
        models.APIServiceLog.objects.filter(created__lt=days_for_deletion).delete()
