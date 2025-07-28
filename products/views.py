# products/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.exceptions import NotFound
from .models import *
from .serializers import * 
from django.db.models import Q


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
