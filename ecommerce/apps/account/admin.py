from django.contrib import admin

from . import models


@admin.register(models.Customer)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "is_active"]
    list_filter = ["is_active"]
    list_editable = ["is_active"]


admin.site.register(models.Address)
