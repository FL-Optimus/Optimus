from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=200)
    density = models.FloatField(verbose_name='[kg/m^3]')
    e_modulus = models.FloatField(verbose_name='Youngs Modulus')
    yield_strength = models.FloatField(verbose_name='yield strength')
    ultimate_strength = models.FloatField(verbose_name='ultimate strength')
    property = models.JSONField(null=True)

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