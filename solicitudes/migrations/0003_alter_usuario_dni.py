# Generated by Django 4.2.3 on 2023-07-26 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0002_tipousuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.CharField(max_length=8, unique=True),
        ),
    ]
