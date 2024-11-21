from django.db import models

# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.nom
