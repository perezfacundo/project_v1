# Generated by Django 4.2.2 on 2023-07-05 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0005_alter_solicitud_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitud',
            name='fechaTrabajo',
            field=models.DateTimeField(help_text='Fecha que desea'),
        ),
    ]
