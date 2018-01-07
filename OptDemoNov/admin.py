from django.contrib import admin

# Register your models here.

from .models import Truck
from .models import SysUsers

admin.site.register(Truck)
admin.site.register(SysUsers)
