# Generated by Django 4.2.7 on 2023-11-29 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0016_rename_pago_faltante_solicitud_ha_pagado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='administrativo',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
