from django.contrib import admin
from .models import Airfoil, Blade, Generator
# Register your models here.
admin.site.register(Airfoil)
admin.site.register(Blade)
admin.site.register(Generator)
