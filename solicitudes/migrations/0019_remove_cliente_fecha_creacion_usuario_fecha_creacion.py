# Generated by Django 4.2.7 on 2023-12-09 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0018_cliente_fecha_creacion_vehiculo_kilometraje_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='fecha_creacion',
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
    ]
