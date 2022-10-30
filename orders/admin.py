from django.contrib import admin
from .models import Payment, Address, Order, OrderProduct

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'order', 'payment', 'product', 'quantity', 'ordered', 'created_at', 'updated_at']

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'product_price', 'quantity')

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

admin.site.register(Payment)
admin.site.register(Address)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)