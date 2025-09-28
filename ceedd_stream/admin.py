from django.contrib import admin
from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo

# Register your models here.
@admin.register(ZoneContributive)
class ZoneContributiveAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'created_at', 'updated_at')
    search_fields = ('nom', 'description')
    ordering = ('nom',)
