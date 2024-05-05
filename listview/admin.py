from django.contrib import admin

# Register your models here.
from . models import Client, Base_Email

admin.site.register(Client)
admin.site.register(Base_Email)


# class CustomerAdmin(admin.ModelAdmin):
#   list_display = ['id', name]