# Generated by Django 3.1.6 on 2021-02-17 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WindTurbine', '0002_airfoil'),
    ]

    operations = [
        migrations.AddField(
            model_name='blade',
            name='airfoils',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='WindTurbine.airfoil'),
            preserve_default=False,
        ),
    ]
