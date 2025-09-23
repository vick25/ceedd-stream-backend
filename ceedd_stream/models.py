from django.contrib.gis.db import models
from django.utils import timezone

class ZonesContributive(models.Model):
    nom = models.CharField(max_length=255)
    superficie = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    etat_ravin = models.CharField(max_length=50, choices=[('actif','Actif'), ('stable','Stable')], blank=True)
    shapefile_id = models.IntegerField(null=True, blank=True)
    geom = models.PolygonField(srid=4326)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom


class Bailleur(models.Model):
    nom = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom


class TypeInfrastructure(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    symbole = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    prenom = models.CharField(max_length=255, blank=True)
    sexe = models.CharField(max_length=1, choices=[('M','Masculin'), ('F','Féminin')], blank=False)
    date_naissance = models.DateField(null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(unique=True, blank=True)
    avenue = models.CharField(max_length=255, blank=True)
    quartier = models.CharField(max_length=255, blank=True)
    commune = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.prenom} {self.nom}".strip()


class Infrastructure(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    capacite = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    date_verification = models.DateField(null=True, blank=True)
    annee_construction = models.IntegerField(null=True, blank=True)
    mois = models.CharField(max_length=20, blank=True)
    trimestre = models.CharField(max_length=20, blank=True)
    type_infrastructure = models.ForeignKey(TypeInfrastructure, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    zone = models.ForeignKey(ZonesContributive, null=True, blank=True, on_delete=models.SET_NULL)
    latitude = models.PointField(srid=4326)
    longitude = models.PointField(srid=4326)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nom or f"Infrastructure {self.id}"


class Finance(models.Model):
    bailleur = models.ForeignKey(Bailleur, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    date_financement = models.DateTimeField(default=timezone.now)
    montant = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('bailleur', 'infrastructure')


class Inspection(models.Model):
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE, related_name="inspections")
    date = models.DateTimeField(default=timezone.now)
    etat = models.CharField(
        max_length=50,
        choices=[('bon', 'Bon'), ('moyen', 'Moyen'), ('mauvais', 'Mauvais')]
    )
    inspecteur = models.CharField(max_length=255, blank=True)
    commentaire = models.TextField(blank=True)
    prochain_controle = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Inspection {self.id} - {self.infrastructure}"


class Photo(models.Model):
    ENTITY_CHOICES = [
        ('infrastructure', 'Infrastructure'),
        ('bailleur', 'Bailleur'),
        ('zone_contributive', 'Zone contributive'),
        ('inspection', 'Inspection'),
    ]
    entity_type = models.CharField(max_length=50, choices=ENTITY_CHOICES)
    entity_id = models.IntegerField()
    url = models.TextField()
    description = models.TextField(blank=True)
    date_prise = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Role(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('contributeur', 'Contributeur'),
        ('lecteur', 'Lecteur'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.role


class Utilisateur(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.TextField()
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
