from django.contrib import admin
from .models import Products
from .models import Order
# Register your models here.

admin.site.site_header = 'E-commerce Site'
admin.site.site_title = 'E-comm Shop'

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'category', 'description', 'image',)
    search_fields = ('title',)

admin.site.register(Products, ProductAdmin)
admin.site.register(Order)