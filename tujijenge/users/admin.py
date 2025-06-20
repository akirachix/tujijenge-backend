from django.contrib import admin
 
# Register your models here.

from .models import Mamamboga
from .models import Stakeholder
admin.site.register(Mamamboga)
admin.site.register(Stakeholder)
