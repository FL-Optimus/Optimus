from django.db import models
from django_mysql.models import JSONField

# Create your models here.

class Airfoil(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.JSONField()
    polar = models.JSONField()

    def __str__(self):
        return self.name


class Blade(models.Model):
    name = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    airfoil = models.ManyToManyField(Airfoil)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
