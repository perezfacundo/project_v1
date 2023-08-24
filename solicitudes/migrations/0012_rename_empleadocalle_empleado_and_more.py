# Generated by Django 4.2.3 on 2023-08-23 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0011_rename_estadostransporte_estadosvehiculo_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='EmpleadoCalle',
            new_name='Empleado',
        ),
        migrations.RenameModel(
            old_name='EstadosEmpleadoCalle',
            new_name='EstadosEmpleado',
        ),
        migrations.RenameModel(
            old_name='tipo_usuario',
            new_name='TiposUsuario',
        ),
        migrations.AlterModelOptions(
            name='empleado',
            options={'verbose_name_plural': 'Empleados'},
        ),
        migrations.AlterModelOptions(
            name='estadosempleado',
            options={'verbose_name_plural': 'Estados de empleados'},
        ),
        migrations.RenameField(
            model_name='empleado',
            old_name='id_estado_empleado_calle',
            new_name='id_estado_empleado',
        ),
    ]
