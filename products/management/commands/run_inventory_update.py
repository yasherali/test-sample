from django.core.management.base import BaseCommand
from products.tasks import *
from celery import chain

class Command(BaseCommand):
    help = 'Runs the nightly inventory update task chain'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Triggering nightly inventory update task chain..."))

        chain(
            import_csv_data.s(),
            validate_and_update.s(),
            generate_report_and_email.s()
        ).delay()

        self.stdout.write(self.style.SUCCESS("Task chain triggered successfully via Celery."))
