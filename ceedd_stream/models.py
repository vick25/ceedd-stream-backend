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
    geom = models.PolygonField(srid=4326, null=True, blank=True)
    shapefile_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Bailleur(models.Model):
    nom = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class TypeInfrastructure(models.Model):
    nom = models.CharField(max_length=255, unique=True)
    symbole = models.BinaryField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Client(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    prenom = models.CharField(max_length=255, blank=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True)
    avenue = models.CharField(max_length=255, blank=True)
    quartier = models.CharField(max_length=255, blank=True)
    commune = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}".strip()


class Infrastructure(models.Model):
    nom = models.CharField(max_length=255, blank=True)
    capacite = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    unite = models.CharField(max_length=20, blank=True)
    date_construction = models.DateField(null=True, blank=True)
    latitude = models.PointField(srid=4326)
    longitude = models.PointField(srid=4326)
    type_infrastructure = models.ForeignKey(TypeInfrastructure, null=True, blank=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    zone = models.ForeignKey(ZoneContributive, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom or f"Infrastructure {self.id}"


class Finance(models.Model):
    bailleur = models.ForeignKey(Bailleur, on_delete=models.CASCADE)
    infrastructure = models.ForeignKey(Infrastructure, on_delete=models.CASCADE)
    date_financement = models.DateTimeField(default=timezone.now)
    montant = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    class Meta:
        unique_together = ('bailleur', 'infrastructure')

    def __str__(self):
        return f"{self.bailleur} -> {self.infrastructure}"


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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inspection {self.id} - {self.infrastructure}"


class Photo(models.Model):
    ENTITE_CHOICES = [
        ('infrastructure', 'Infrastructure'),
        ('bailleur', 'Bailleur'),
        ('zone_contributive', 'Zone contributive'),
        ('inspection', 'Inspection'),
    ]
    entite_type = models.CharField(max_length=50, choices=ENTITE_CHOICES)
    entite_id = models.IntegerField()
    url = models.TextField()
    description = models.TextField(blank=True)
    date_prise = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.entite_type} #{self.entite_id}"


class Role(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('contributeur', 'Contributeur'),
        ('lecteur', 'Lecteur'),
    ]
    role = models.CharField(max_length=20, choices=ROLES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.role


class Utilisateur(models.Model):
    nom = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mot_de_passe = models.TextField()
    role = models.ForeignKey(Role, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
