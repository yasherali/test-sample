import csv
from celery import shared_task, chain
from .models import Product
from django.core.mail import send_mail
from django.conf import settings
from io import StringIO
import os

CSV_FILE_PATH = os.path.join(settings.BASE_DIR, 'mock_data/products.csv')

@shared_task
def import_csv_data():
    with open(CSV_FILE_PATH, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    return rows

@shared_task
def validate_and_update(data):
    updated = 0
    for row in data:
        try:
            product = Product.objects.get(sku=row['sku'])
            product.quantity = int(row['quantity'])
            product.save()
            updated += 1
        except Product.DoesNotExist:
            continue
    return updated

@shared_task
def generate_report_and_email(updated_count):
    body = f"{updated_count} products were updated in inventory."
    send_mail(
        subject="Inventory Update Report",
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=["admin@yopmail.com"],  # Update as needed
        fail_silently=False
    )
