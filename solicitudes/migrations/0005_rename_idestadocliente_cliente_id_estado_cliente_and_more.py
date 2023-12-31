# Generated by Django 4.2.3 on 2023-08-15 22:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0004_remove_solicitud_desde_remove_solicitud_hasta_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='idEstadoCliente',
            new_name='id_estado_cliente',
        ),
        migrations.RenameField(
            model_name='empleadoadministrativo',
            old_name='idEstadoEmpleadoAdministrativo',
            new_name='id_estado_empleado_administrativo',
        ),
        migrations.RenameField(
            model_name='empleadocalle',
            old_name='idEstadoEmpleadoCalle',
            new_name='id_estado_empleado_calle',
        ),
        migrations.RenameField(
            model_name='empleadocalle',
            old_name='tipoCarnet',
            new_name='tipo_carnet',
        ),
        migrations.RenameField(
            model_name='solicitud',
            old_name='fechaSolicitud',
            new_name='fecha_solicitud',
        ),
        migrations.RenameField(
            model_name='solicitud',
            old_name='fechaTrabajo',
            new_name='fecha_trabajo',
        ),
        migrations.RenameField(
            model_name='solicitud',
            old_name='idEstadoSolicitud',
            new_name='id_estado_solicitud',
        ),
        migrations.RenameField(
            model_name='solicitud',
            old_name='pagoFaltante',
            new_name='pago_faltante',
        ),
        migrations.RenameField(
            model_name='solicitudesempleados',
            old_name='idEmpleado',
            new_name='id_empleado',
        ),
        migrations.RenameField(
            model_name='solicitudesempleados',
            old_name='idSolicitud',
            new_name='id_solicitud',
        ),
        migrations.RenameField(
            model_name='solicitudestransportes',
            old_name='idSolicitud',
            new_name='id_solicitud',
        ),
        migrations.RenameField(
            model_name='solicitudestransportes',
            old_name='idTransporte',
            new_name='id_transporte',
        ),
        migrations.RenameField(
            model_name='transporte',
            old_name='idEstadoTransporte',
            new_name='id_estado_transporte',
        ),
        migrations.RenameField(
            model_name='usuario',
            old_name='idTipoUsuario',
            new_name='id_tipo_usuario',
        ),
    ]
