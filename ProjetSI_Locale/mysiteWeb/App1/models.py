from django.db import models

class Whitelist(models.Model):
    mail = models.CharField(max_length=255)
    statut = models.CharField(max_length=60)

    class Meta:
        db_table = 'whitelist'


class Blacklist(models.Model):
    mail = models.CharField(max_length=255)
    statut = models.CharField(max_length=60)

    class Meta:
        db_table = 'blacklist'


class Appointment(models.Model):
    mail = models.EmailField(max_length=255)  # Champ pour stocker les adresses email
    idbox = models.IntegerField(default=1, primary_key=True)
    date = models.DateField()  # Date de l'appartement
    entry_time = models.TimeField()  # Heure de début
    exit_time = models.TimeField()  # Heure de fin


    class Meta:
        db_table = 'Appointment'