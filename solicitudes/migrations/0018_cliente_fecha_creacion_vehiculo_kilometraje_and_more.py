# Generated by Django 4.2.7 on 2023-12-09 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0017_empleado_administrativo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='fecha_creacion',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='kilometraje',
            field=models.IntegerField(default='0', null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='puntos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='capacidad',
            field=models.IntegerField(null=True),
        ),
    ]
