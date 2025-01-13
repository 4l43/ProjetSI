from django.db import models

class Whitelist(models.Model):
    mail = models.CharField(max_length=255)
    statut = models.CharField(max_length=60)

    class Meta:
        db_table = 'whitelist'
