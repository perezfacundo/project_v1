# Generated by Django 4.2.2 on 2023-06-22 01:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desde', models.CharField(max_length=50)),
                ('hasta', models.CharField(max_length=50)),
                ('fechaSolicitud', models.DateTimeField(auto_now_add=True)),
                ('fechaTrabajo', models.DateTimeField()),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.estado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
