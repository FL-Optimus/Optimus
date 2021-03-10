from django.db import models

# Create your models here.
class Blade(models.Model):
    name = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

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

    def __str__(self):
        return self.name + ' ' + self.rated_power + ' MW'
