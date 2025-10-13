from django.contrib import admin
from django.contrib.gis import admin
from django.contrib.gis import forms
from leaflet.forms.widgets import LeafletWidget
from leaflet.admin import LeafletGeoAdmin
from .models import ZoneContributive, Bailleur, TypeInfrastructure, Client, Infrastructure, Finance, Inspection, Photo

admin.site.site_header = "CEEDD Stream Backend Administration"
admin.site.site_title = "CEEDD Stream Admin Portal"
admin.site.index_title = "Welcome to CEEDD Stream Admin Portal"

# Register your models here.
@admin.register(ZoneContributive)
class ZoneContributiveAdmin(LeafletGeoAdmin):
    list_display = ('nom', 'description', 'created_at', 'updated_at')
    search_fields = ('nom', 'description')
    ordering = ('-updated_at',)
    list_display_links = ('nom',)

admin.site.register(Bailleur)
admin.site.register(TypeInfrastructure)
admin.site.register(Client)

class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = '__all__'
        widgets = {
            'location': LeafletWidget(attrs={'map_width': '800px', 'map_height': '100%'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        point = cleaned_data.get('location')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')

        # Case 1: if point exists → update lat/lon fields
        if point:
            cleaned_data['latitude'] = point.y
            cleaned_data['longitude'] = point.x

        # Case 2: if lat/lon manually entered → rebuild Point geometry
        elif latitude and longitude:
            from django.contrib.gis.geos import Point
            cleaned_data['location'] = Point(float(longitude), float(latitude), srid=4326)

        return cleaned_data

@admin.register(Infrastructure)
class InfrastructureAdmin(LeafletGeoAdmin):
    form = LocationAdminForm
    list_display = ('nom', 'type_infrastructure', 'client', 'zone', 'created_at', 'updated_at')
    search_fields = ('nom', 'type_infrastructure__nom', 'client__nom', 'zone__nom')
    ordering = ('-updated_at',)
    list_display_links = ('client',)
    list_filter = ('type_infrastructure', 'client', 'zone')

admin.site.register(Finance)
admin.site.register(Inspection)
admin.site.register(Photo)
#admin.site.register(Role)