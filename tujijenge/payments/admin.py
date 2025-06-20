from django.contrib import admin

from .models import Payment
admin.site.register(Payment)

from .models import Order
admin.site.register(Order)

