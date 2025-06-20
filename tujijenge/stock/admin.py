from django.contrib import admin
from .models import Stock
from .models import Product

admin.site.register(Stock)
admin.site.register(Product)
