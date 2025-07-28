from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='product-api'),
]