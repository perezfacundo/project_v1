# Generated by Django 4.2.3 on 2023-10-13 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0015_remove_solicitud_coordenadas_desde_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitud',
            old_name='pago_faltante',
            new_name='ha_pagado',
        ),
        migrations.AddField(
            model_name='solicitud',
            name='presupuesto',
            field=models.IntegerField(null=True),
        ),
    ]
