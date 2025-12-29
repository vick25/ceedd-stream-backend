from django.contrib import admin

# from django.contrib.gis import admin
from django.contrib.gis import forms

# from leaflet.forms.widgets import LeafletWidget
from leaflet.admin import LeafletGeoAdmin

from .models import (
    Bailleur,
    Client,
    Finance,
    Infrastructure,
    Inspection,
    Photo,
    TypeInfrastructure,
    ZoneContributive,
)

admin.site.site_header = "CEEDD Stream Backend Administration"
admin.site.site_title = "CEEDD Stream Admin Portal"
admin.site.index_title = "Welcome to CEEDD Stream Admin Portal"


# Register your models here.
@admin.register(ZoneContributive)
class ZoneContributiveAdmin(LeafletGeoAdmin):
    list_display = ("nom", "description", "created_at", "updated_at")
    search_fields = ("nom", "description")
    ordering = ("-updated_at",)
    list_display_links = ("nom",)


class BailleurAdmin(admin.ModelAdmin):
    list_display = ("nom", "created_at", "updated_at")
    search_fields = ("nom",)
    ordering = ("-updated_at",)


admin.site.register(Bailleur, BailleurAdmin)


class TypeInfrastructureAdmin(admin.ModelAdmin):
    list_display = ("nom", "description", "created_at", "updated_at")
    search_fields = ("nom", "description")
    ordering = ("-updated_at",)


admin.site.register(TypeInfrastructure, TypeInfrastructureAdmin)


class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "titre",
        "nom",
        "postnom",
        "prenom",
        "quartier",
        "commune",
        "engagement",
        "created_at",
        "updated_at",
    )
    search_fields = ("nom", "postnom", "prenom", "quartier", "commune")
    ordering = ("-updated_at",)
    list_display_links = ("nom", "prenom")
    list_editable = ("engagement",)
    list_per_page = 10


admin.site.register(Client, ClientAdmin)


class LocationAdminForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = "__all__"
        # widgets = {
        #     'location': LeafletWidget(),
        # }

    def clean(self):
        cleaned_data = super().clean()
        point = cleaned_data.get("location")
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")

        # Case 1: if point exists → update lat/lon fields
        if point:
            cleaned_data["latitude"] = point.y
            cleaned_data["longitude"] = point.x

        # Case 2: if lat/lon manually entered → rebuild Point geometry
        elif latitude and longitude:
            from django.contrib.gis.geos import Point

            cleaned_data["location"] = Point(
                float(longitude), float(latitude), srid=4326
            )

        return cleaned_data


@admin.register(Infrastructure)
class InfrastructureAdmin(LeafletGeoAdmin):
    form = LocationAdminForm
    list_display = (
        "client__nom",
        "nom",
        "type_infrastructure__nom",
        "zone__nom",
        "latitude",
        "longitude",
        "date_construction",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "nom",
        "date_construction",
        "type_infrastructure__nom",
        "client__nom",
        "zone__nom",
    )
    ordering = ("-updated_at",)
    list_display_links = ("nom", "client__nom")
    list_filter = (
        "type_infrastructure",
        "zone",
        "date_construction",
    )


class FinanceAdmin(admin.ModelAdmin):
    list_display = (
        "infrastructure__nom",
        "bailleur__nom",
        "montant",
        "date_financement",
    )
    search_fields = ("infrastructure__nom", "bailleur__nom")
    ordering = ("-date_financement",)


admin.site.register(Finance, FinanceAdmin)


class InspectionAdmin(admin.ModelAdmin):
    list_display = (
        "infrastructure__nom",
        "date",
        "etat",
        "inspecteur",
        "created_at",
        "updated_at",
    )
    search_fields = ("infrastructure__nom", "inspecteur")
    ordering = ("-updated_at",)
    list_filter = ("etat",)


admin.site.register(Inspection, InspectionAdmin)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ("content_object", "url", "date_prise", "numero_photo", "created_at")
    search_fields = ("url", "date_prise", "numero_photo")
    list_filter = ("content_type",)
    readonly_fields = ("content_type", "object_id", "content_object")


admin.site.register(Photo, PhotoAdmin)

# admin.site.register(Role)
