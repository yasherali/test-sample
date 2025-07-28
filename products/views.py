# products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound

from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import *
from .serializers import * 
from .permissions import *
from .utils import *

import json


class ProductAPIView(APIView):
    permission_classes = [IsAPIUser]

    def get(self, request):
        queryset = Product.objects.all().order_by('-updated_at')
        
        sku = request.GET.get('sku')
        price = request.GET.get('price')
        quantity = request.GET.get('quantity')
        search = request.GET.get('search')

        if sku:
            queryset = queryset.filter(sku=sku)
        if price:
            queryset = queryset.filter(price=price)
        if quantity:
            queryset = queryset.filter(quantity=quantity)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(sku__icontains=search))

        paginator = LimitOffsetPagination()
        paginated_qs = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        sku = request.data.get('sku')
        if not sku:
            return Response({"error": "SKU is required to update a product."}, status=400)
        try:
            product = Product.objects.get(sku=sku)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        sku = request.data.get('sku')
        if not sku:
            return Response({"error": "SKU is required to delete a product."}, status=400)
        try:
            product = Product.objects.get(sku=sku)
            product.delete()
            return Response({"success": "Product deleted."}, status=204)
        except Product.DoesNotExist:
            raise NotFound("Product not found.")

@method_decorator(csrf_exempt, name='dispatch')
class ShopifyWebhookAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # You can change this if needed

    def post(self, request, *args, **kwargs):
        hmac_header = request.META.get('HTTP_X_SHOPIFY_HMAC_SHA256')
        body = request.body.decode('utf-8')

        if not is_valid_shopify_hmac(body, hmac_header):
            return Response({'error': 'Invalid HMAC'}, status=status.HTTP_403_FORBIDDEN)

        try:
            payload = json.loads(body)
            sku = payload.get('sku')
            quantity = payload.get('quantity')

            if not sku or quantity is None:
                return Response({'error': 'Invalid payload data'}, status=status.HTTP_400_BAD_REQUEST)

            product = Product.objects.get(sku=sku)
            product.quantity = quantity
            product.save()

            return Response({'status': 'updated'}, status=status.HTTP_200_OK)

        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)