from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.TgUser)
admin.site.register(models.Service)
admin.site.register(models.TgOrders)


