from django.contrib import admin
from .models import *

# Register your models her
# superuser:RangeAuto
admin.site.register(Firer)
admin.site.register(Result)
admin.site.register(Detail)
admin.site.register(Fire)
admin.site.site_header = "Digital Range Management System"
