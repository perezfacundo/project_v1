# Generated by Django 4.2.3 on 2023-09-06 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0012_rename_empleadocalle_empleado_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='dominio',
            field=models.CharField(max_length=7, unique=True),
        ),
    ]