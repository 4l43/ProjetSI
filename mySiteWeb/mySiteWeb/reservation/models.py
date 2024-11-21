from django.db import models

# Create your models here.

class Utilisateur(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Task(models.Model):
    title = models.CharField(Max_length=200)
    description = models.TextField(blank=True)
    completed = models.booleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title