from django.db import models
from django_mysql.models import JSONField


class Material(models.Model):
    name = models.CharField(max_length=200)
    density = models.FloatField(verbose_name='[kg/m^3]')
    e_modulus = models.FloatField(verbose_name='Youngs Modulus')
    yield_strength = models.FloatField(verbose_name='yield strength')
    ultimate_strength = models.FloatField(verbose_name='ultimate strength')
    property = models.JSONField(null=True)
# Create your models here.

class Airfoil(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.JSONField()
    polar = models.JSONField()
    thickness = models.DecimalField(max_digits=4, decimal_places=2)
    thickness_loc = models.DecimalField(max_digits=4, decimal_places=2)
    camber = models.DecimalField(max_digits=4, decimal_places=2)
    camber_loc = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class Blade(models.Model):
    name = models.CharField(max_length=255)
    length = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='[m]')
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='[kg]')
    root_diameter = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='[m]')
    number_of_bolts = models.IntegerField()
    bolt_hole_diameter = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='[mm]')

    def __str__(self):
        return self.name

class Generator(models.Model):
    name = models.CharField(max_length=255)
    rated_power = models.DecimalField(max_digits=5, decimal_places=2)
    reted_torque = models.DecimalField(max_digits=5, decimal_places=2)
    gen_type = models.CharField(max_length=255)
    efficiency = models.DecimalField(max_digits=5, decimal_places=2)
    pole_pairs = models.IntegerField()
    image = models.ImageField(upload_to='generator')

    length = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    airfoil = models.ManyToManyField(Airfoil)

    def __str__(self):
        return self.name + ' ' + self.rated_power + ' MW'

    class Meta:
        ordering = ['name']
