from django.contrib.gis.db import models
from django.utils import timezone


class ZoneContributive(models.Model):
    nom = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    etat_ravin = models.CharField(
        max_length=50,
        choices=[('actif', 'Actif'), ('stable', 'Stable')],
        blank=True
    )
    description = models.TextField(blank=True)
    geom = models.PolygonField(srid=4326, null=True, blank=True)
    shapefile_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Bailleur(models.Model):
    nom = models.CharField(max_length=255)
    sigle = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class TypeInfrastructure(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    postnom = models.CharField(max_length=255, null=True, blank=True)
    prenom = models.CharField(max_length=255, null=True, blank=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    quartier = models.CharField(max_length=255, null=True, blank=True)
    numero = models.IntegerField(null=True, blank=True)
    telephone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    commune = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}".strip()


class Infrastructure(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    capacite = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unite = models.CharField(max_length=20, blank=True)
    date_construction = models.DateField(null=True, blank=True)
    location = models.PointField(srid=4326, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    type_infrastructure = models.ForeignKey(TypeInfrastructure, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    zone = models.ForeignKey(ZoneContributive, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom or f"Infrastructure {self.id}"

    def save(self, *args, **kwargs):
        if self.location is None and self.latitude is not None and self.longitude is not None:
            from django.contrib.gis.geos import Point
            self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)



class Finance(models.Model):
    bailleur = models.ForeignKey(Bailleur, related_name="finances", on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    date_financement = models.DateTimeField(default=timezone.now, null=True, blank=True)
    montant = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unite_monnaie = models.CharField(max_length=10,
                                     choices=[('Fc', 'Franc Congolais'), ('$', 'Dollars US'), ('€', 'Euros')],
                                     default='Fc', null=True, blank=True)

    class Meta:
        unique_together = ('bailleur', 'infrastructure')

    def __str__(self):
        return f"{self.bailleur} -> {self.infrastructure}"


class Inspection(models.Model):
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, related_name="inspections")
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    etat = models.CharField(
        max_length=50,
        choices=[('bon', 'Bon'), ('moyen', 'Moyen'), ('mauvais', 'Mauvais')],
        default='bon', null=True, blank=True
    )
    inspecteur = models.CharField(max_length=255, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)
    prochain_controle = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inspection {self.id} - {self.infrastructure}"


class Photo(models.Model):
    # Fields for generic relation
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True) # which model
    object_id = models.PositiveIntegerField(null=True) # which row inside that model
    content_object = GenericForeignKey('content_type', 'object_id') # actual object like Infrastructure(id=12)

    url = models.TextField()
    description = models.TextField(null=True, blank=True)
    date_prise = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photo for {self.content_object}"


# class Role(models.Model):
#     ROLES = [
#         ('admin', 'Admin'),
#         ('contributeur', 'Contributeur'),
#         ('lecteur', 'Lecteur'),
#     ]
#     role = models.CharField(max_length=20, choices=ROLES, unique=True, default='lecteur')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.role


# class Utilisateur(models.Model):
#     nom = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     mot_de_passe = models.TextField()
#     role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.email
