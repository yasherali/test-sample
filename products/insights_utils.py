# product/insights_utils.py
from datetime import timedelta
from django.utils import timezone
from .models import Product

def get_low_stock_stats(threshold=5):
    total = Product.objects.count()
    low = Product.objects.filter(quantity__lt=threshold).count()
    percent = (low / total) * 100 if total else 0
    return {
        "low_stock_count": low,
        "total_products": total,
        "low_stock_percent": round(percent, 2)
    }

def get_trending_products(hours=48):
    since = timezone.now() - timedelta(hours=hours)
    return Product.objects.filter(updated_at__gte=since).order_by('-updated_at')
