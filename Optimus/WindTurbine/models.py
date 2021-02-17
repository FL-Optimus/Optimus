from django.db import models

# Create your models here.
class Blade(models.Model):
    name = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name