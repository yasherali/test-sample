from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product-api'),
    path('webhook/shopify/', ShopifyWebhookAPIView.as_view(), name='shopify-webhook'),
    path('products/search/', SmartProductSearchAPIView.as_view(), name='smart_product_search'),
    path('products/insights/', ProductInsightsAPIView.as_view(), name='product_insights'),
]