from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'quantity', 'updated_at']
    list_filter = ['updated_at', 'sku', 'name']
    search_fields = ['name', 'sku']
    actions = ['bulk_price_update']

    def bulk_price_update(self, request, queryset):
        for product in queryset:
            product.price += 10  
            product.save()
        self.message_user(request, "Prices updated.")
    bulk_price_update.short_description = "Increase price by 10"