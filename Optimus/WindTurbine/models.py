import json

from django.db import models
from django.db.models.deletion import CASCADE
from django_mysql.models import JSONField


class Material(models.Model):
    name = models.CharField(max_length=200)
    density = models.FloatField(verbose_name='[kg/m^3]')
    e_modulus = models.FloatField(verbose_name='Youngs Modulus')
    yield_strength = models.FloatField(verbose_name='yield strength')
    ultimate_strength = models.FloatField(verbose_name='ultimate strength')
    property = models.JSONField(null=True)


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

class Airfoil(models.Model):
    name = models.CharField(max_length=255)
    geometry = models.JSONField(blank=True, null=True)
    polar = models.JSONField(blank=True, null=True)
    # thickness = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    # thickness_loc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    # camber = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    # camber_loc = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    blade = models.ForeignKey(Blade, on_delete=CASCADE)

    def split_airfoil(self):
        x = (json.loads(self.geometry)['x'])
        y = (json.loads(self.geometry)['y'])

        end_value = int(len(x)/2)
        positive_part = y[:end_value]
        negative_part = y[end_value:][::-1]
        return list(zip(positive_part, negative_part))

    def camber(self):
        data = self.split_airfoil()
        camber = [(a+b)/2 for a,b in data]
        value = f'{max(camber) * 100 :.2f}'
        location = camber.index(max(camber))        
        location = f'{100- camber.index(max(camber))/len(data)*100 :.2f}'
        return {'value': value, 'location': location}

    def thickness(self):
        data = self.split_airfoil()
        thickness = [a-b for a,b in data]
        value = f'{max(thickness) * 100 :.2f}'
        location = f'{100- thickness.index(max(thickness))/len(data)*100 :.2f}'
        return {'value': value,  'location': location}      

    def polars(self):
        pass

    def __str__(self):
        if self.name:
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
