# Generated by Django 4.2.3 on 2023-08-20 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0007_solicitud_cliente_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleadoadministrativo',
            name='fecha_nac',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='empleadocalle',
            name='fecha_nac',
            field=models.DateField(null=True),
        ),
    ]