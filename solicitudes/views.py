from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError, transaction
from .models import (
    Usuario,
    EstadosCliente,
    Cliente,
    EstadosEmpleado,
    Empleado,
    TiposUsuario,
    EstadosSolicitud,
    Solicitud,
    EstadosVehiculo,
    Vehiculo,
    SolicitudesEmpleados,
    SolicitudesVehiculos,
)
from django.contrib.auth.decorators import login_required
import re
import requests
import pandas as pd
from datetime import datetime, timedelta, date
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_protect
from django.urls import reverse
import random
from django.core.mail import send_mail, EmailMessage
import ssl
from django.conf import settings
from dateutil.relativedelta import relativedelta

# VISTAS AUTENTICACION


def home(request):
    logout(request)

    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "auth/signup.html")
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                id_estado_cliente = request.POST.get("id_estado_cliente", None)
                id_tipo_usuario = request.POST.get("id_tipo_usuario", None)

                cliente = Cliente.objects.create_user(
                    first_name=request.POST["first_name"],
                    last_name=request.POST["last_name"],
                    username=request.POST["username"],
                    password=request.POST["password1"],
                    email=request.POST["email"],
                    dni=request.POST["dni"],
                    telefono=request.POST["telefono"],
                    id_estado_cliente=EstadosCliente.objects.get(id=id_estado_cliente),
                    id_tipo_usuario=TiposUsuario.objects.get(id=id_tipo_usuario),
                    fecha_nac=request.POST["fecha_nac"],
                    fecha_creacion=date.today(),
                    puntos=0,
                )
                cliente.save()
                login(request, cliente)
                request.session["username"] = cliente.username
                return redirect("solicitudes")
            except Exception as e:
                print("Error en signup:", e)
                return render(
                    request,
                    "auth/signup.html",
                    {"error": "Ocurrio un error al registrar el usuario."},
                )
        return render(request, "auth/signup.html", {"error": "Las claves no coinciden"})


def signin(request):
    if request.method == "GET":
        return render(request, "auth/signin.html", {"form": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            return render(
                request,
                "auth/signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "El usuario o la contraseña son incorrectos",
                },
            )
        else:
            login(request, user)
            request.session["username"] = user.username

            objUsuario = Usuario.objects.get(username=request.session["username"])
            if objUsuario.id_tipo_usuario.descripcion == "Cliente" or objUsuario.id_tipo_usuario.descripcion == "Empleado":
                return redirect("solicitudes")
            else:
                return redirect("dashboard")


def recuperarCuenta(request):
    if request.method == "GET":
        return render(request, "auth/recuperarCuenta.html")
    elif request.method == "POST":
        # Generar codigo
        codigo = str(random.randint(100000, 999999))
        print("El codigo es " + codigo)
        request.session["codigoRecuperacion"] = codigo
        request.session["momentoGeneracionCodigo"] = datetime.now().isoformat()
        request.session["correo"] = request.POST["email"]

        try:
            objUsuario = Usuario.objects.get(email=request.POST["email"])
            print(objUsuario)

            request.session["username"] = objUsuario.username
            print(request.session["username"])

            # Enviar correo con formato normal
            subject = "Acá está tu código"
            message = (
                "El código es "
                + codigo
                + ". Te avisamos que será válido por sólo 15 minutos."
            )
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [request.POST["email"]]
            send_mail(subject, message, from_email, recipient_list)

            # Para enviar correos con formato HTML
            # email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            # email.content_subtype = 'html'

            # # Agrega el contenido HTML directamente al cuerpo del correo
            # html_content = '<div style="background-color: black"><h1 style="font-size: 100%;"> FLETTER </h1></div>'

            # html_content += f'<p style="font-size: 20px;"> {message} </p>'
            # html_content += '<p> Si no tienes una cuenta de fletter o crees que este correo fue enviado por error, solo ignóralo. Saludos !</p>'
            # email.body = html_content

            # email.send()

            return redirect("ingresarCodigoRecuperacion")
        except Exception as e:
            return render(
                request,
                "auth/recuperarCuenta.html",
                {"error": "El correo no pertenece a ningun usuario registrado."},
            )


def ingresarCodigoRecuperacion(request):
    if request.method == "GET":
        return render(request, "auth/ingresarCodigoRecuperacion.html")

    elif request.method == "POST":
        limite_de_tiempo = timedelta(minutes=15)
        fecha_y_hora_actual = datetime.now()
        momentoGeneracionCodigo = datetime.fromisoformat(
            request.session["momentoGeneracionCodigo"]
        )

        diferencia = fecha_y_hora_actual - momentoGeneracionCodigo

        if diferencia < limite_de_tiempo:
            if (
                request.POST["codigoRecuperacion"]
                == request.session["codigoRecuperacion"]
            ):
                return redirect("cambiarClave")
            else:
                return render(
                    request,
                    "auth/ingresarCodigoRecuperacion",
                    {"error": "No hay coincidencia. Intente de nuevo"},
                )
        else:
            return render(
                request,
                "auth/ingresarCodigoRecuperacion",
                {
                    "error": "Se cumplieron los 15 minutos de validez del código. Intente de nuevo."
                },
            )


def cambiarClave(request):
    if request.method == "GET":
        return render(request, "auth/cambiarClave.html")
    elif request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            try:
                objUsuario = Usuario.objects.get(email=request.session["correo"])
            except:
                objUsuario = Usuario.objects.get(username=request.session["username"])

            objUsuario.set_password(request.POST["password1"])
            objUsuario.save()

            user = authenticate(
                request,
                username=objUsuario.username,
                password=request.POST["password1"],
            )

            if user is None:
                return render(
                    request,
                    "auth/signin.html",
                    {
                        "error": "Ocurrió un error al intentar autenticar la sesión. Intente con la clave nueva."
                    },
                )
            else:
                login(request, user)
                request.session["username"] = objUsuario.username
                return redirect("dashboard")

        else:
            return render(
                request,
                "auth/cambiarClave.html",
                {
                    "error": "La nueva contraseña y la confirmación no coinciden. Intente de nuevo."
                },
            )


@login_required
def signout(request):
    logout(request)
    return redirect("home")


@login_required
def dashboard(request):
    nuevos_clientes = nuevos_clientes_este_mes()
    nuevas_solicitudes = nuevas_solicitudes_este_mes()
    porcentaje = porc_aumento_solicitudes()
    prox_service = vehiculos_prox_service()

    return render(
        request,
        "dashboard.html",
        {
            "nuevos_clientes": nuevos_clientes,
            "nuevas_solicitudes": nuevas_solicitudes,
            "porcentaje_crecimiento": porcentaje,
            "vehiculos_service": prox_service,
        },
    )


def nuevos_clientes_este_mes():
    fecha_actual = date.today()
    fecha_inicio = fecha_actual.replace(day=1)

    cantidad = Cliente.objects.filter(
        fecha_creacion__range=(fecha_inicio, fecha_actual)
    ).count()

    return cantidad


def nuevas_solicitudes_este_mes():
    fecha_actual = date.today()
    fecha_inicio = fecha_actual.replace(day=1)

    cantidad = Solicitud.objects.filter(
        fecha_solicitud__range=(fecha_inicio, fecha_actual)
    ).count()

    return cantidad


def porc_aumento_solicitudes():
    fecha_actual = date.today()
    primer_dia_mes_actual = date(fecha_actual.year, fecha_actual.month, 1)
    ultimo_dia_mes_anterior = date.fromordinal(primer_dia_mes_actual.toordinal() - 1)
    primer_dia_mes_anterior = date(
        ultimo_dia_mes_anterior.year, ultimo_dia_mes_anterior.month, 1
    )

    cantidad_solicitudes_mes_anterior = Solicitud.objects.filter(
        fecha_solicitud__gte=primer_dia_mes_anterior,
        fecha_solicitud__lte=ultimo_dia_mes_anterior,
    ).count()

    cantidad_solicitudes_mes_actual = Solicitud.objects.filter(
        fecha_solicitud__gte=primer_dia_mes_actual, fecha_solicitud__lte=fecha_actual
    ).count()

    try:
        porcentaje = round(
            (cantidad_solicitudes_mes_actual - cantidad_solicitudes_mes_anterior)
            / cantidad_solicitudes_mes_anterior
            * 100,
            2,
        )
    except:
        porcentaje = 0
    return porcentaje


def vehiculos_prox_service():
    necesitan_service = []

    vehiculos = Vehiculo.objects.all()

    fecha_actual = datetime.now().date()

    for vehiculo in vehiculos:
        tiempo_transcurrido = fecha_actual - vehiculo.fecha_ult_service

        if (
            vehiculo.kilometraje_desde_ult_service >= 15000
            or tiempo_transcurrido.days >= 365
        ):
            necesitan_service.append(vehiculo)

    return necesitan_service


def grafico_anual_solicitudes(request):
    meses = [
        "Enero",
        "Febrero",
        "Marzo",
        "Abril",
        "Mayo",
        "Junio",
        "Julio",
        "Agosto",
        "Septiembre",
        "Octubre",
        "Noviembre",
        "Diciembre",
    ]
    cantidades = []
    mes = 1

    while mes <= 12:
        solicitudes_por_mes = Solicitud.objects.filter(
            fecha_solicitud__month=mes
        ).count()

        cantidades.append(solicitudes_por_mes)

        mes += 1

    option = {
        "tooltip": {"show": True, "trigger": "axis", "triggerOn": "mousemove|click"},
        "xAxis": {"type": "category", "data": meses, "axisLabel": {"rotate": 30}},
        "yAxis": {"type": "value"},
        "series": {"data": cantidades, "type": "line", "smooth": True},
    }

    return JsonResponse(option, safe=False)


def grafico_anual_clientes(request):
    data = []

    solicitudes = Solicitud.objects.all()

    clientes_con_solicitudes = (
        solicitudes.values("cliente_id")
        .annotate(num_solicitudes=Count("id"))
        .order_by("-num_solicitudes")[:5]
    )

    for cliente in clientes_con_solicitudes:
        cliente_obj = Cliente.objects.get(pk=cliente["cliente_id"])

        data.append(
            {
                "value": cliente["num_solicitudes"],
                "name": cliente_obj.last_name + " " + cliente_obj.first_name,
            },
        )

    option = {
        "tooltip": {"trigger": "item"},
        "legend": {"top": "5%", "left": "center"},
        "series": [
            {
                "name": "Access From",
                "type": "pie",
                "radius": ["40%", "70%"],
                "avoidLabelOverlap": False,
                "itemStyle": {
                    "borderRadius": 10,
                    "borderColor": "#fff",
                    "borderWidth": 2,
                },
                "label": {"show": False, "position": "center"},
                "emphasis": {
                    "label": {"show": True, "fontSize": 40, "fontWeight": "bold"}
                },
                "labelLine": {"show": False},
                "data": data,
            }
        ],
    }

    return JsonResponse(option, safe=False)


@login_required
def historial_tasas_cambio(request):
    api_key = "373b418d614aa100475b0018"
    base_url = "https://open.er-api.com/v6/exrates/history"

    fecha_actual = datetime.now().date()
    fecha_hace_doce_meses = fecha_actual - timedelta(days=365)

    params = {
        "base_code": "USD",
        "target_code": "ARS",
        "apikey": api_key,
        "start_date": fecha_hace_doce_meses,
        "end_date": fecha_actual,
    }

    print(params)

    try:
        response = requests.get(base_url, params=params)
        print(response.status_code)
        print(response.text)

        data = response.json()

        # Se crea un DataFrame de pandas para facilitar el manejo de datos
        df = pd.DataFrame(data["rates"])
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], unit="s"
        )  # Se convierte el timestamp a formato de fecha

        # Convertir el DataFrame a un formato que se pueda seriealizar a JSON
        historial_json = df.to_json(orient="records", date_format="iso")

        print(historial_json)
        return render(request, "dashboard.html", {"historial_json": historial_json})
    except Exception as e:
        print("El error es: ", e)
        return render(request, "dashboard.html", {"error": str(e)})


# VISTAS SOLICITUDES


@login_required
def solicitudes(request):
    return render(request, "solicitudes/solicitudes.html")


@login_required
def solicitudes_listado(request):

    objUsuario = Usuario.objects.get(username=request.session["username"])
    usuario = objUsuario.to_dict()

    if objUsuario.id_tipo_usuario.descripcion == "Cliente":
        solicitudes = Solicitud.objects.filter(cliente_id=objUsuario.id)
    else:
        solicitudes = Solicitud.objects.all()

    solicitudes_data = [solicitud.to_dict() for solicitud in solicitudes]

    data = {"solicitudes": solicitudes_data, "usuario": usuario}
    return JsonResponse(data, safe=False)


@login_required
@csrf_protect
def solicitudes_prox7dias(
    request,
):  # Solicitudes a realizar dentro de los proximos 7 dias
    print("Listado de solicitudes en los proximos 7 dias")
    print(" ")

    objUsuario = Usuario.objects.get(username=request.session["username"])
    usuario_data = objUsuario.to_dict()

    fechaHoy = datetime.now().date()
    sieteDiasDespues = fechaHoy + timedelta(days=7)

    print(fechaHoy, sieteDiasDespues)

    if objUsuario.id_tipo_usuario.descripcion == "Cliente":
        solicitudes = Solicitud.objects.filter(
            cliente_id=objUsuario.id, fecha_trabajo__range=[fechaHoy, sieteDiasDespues]
        )

    elif objUsuario.id_tipo_usuario.descripcion == "Empleado":
        solicitudes = Solicitud.objects.filter(
            solicitudesempleados__id_empleado=objUsuario.id,
            fecha_trabajo__range=[fechaHoy, sieteDiasDespues],
        )

    elif objUsuario.id_tipo_usuario.descripcion == "Administrador":
        solicitudes = Solicitud.objects.filter(
            fecha_trabajo__range=[fechaHoy, sieteDiasDespues]
        )

    solicitudes_data = [solicitud.to_dict() for solicitud in solicitudes]

    data = {"solicitudes": solicitudes_data, "usuario": usuario_data}

    return JsonResponse(data, safe=False)


@login_required
def solicitudes_pendientes(request):  # Solicitudes que tengan estado pendiente
    print("Listado de solicitudes pendientes")
    print(" ")

    objUsuario = Usuario.objects.get(username=request.session["username"])
    usuario_data = objUsuario.to_dict()

    solicitudes = Solicitud.objects.filter(id_estado_solicitud=1)

    solicitudes_data = [solicitud.to_dict() for solicitud in solicitudes]

    data = {"solicitudes": solicitudes_data, "usuario": usuario_data}

    return JsonResponse(data, safe=False)


@login_required
def solicitudes_crear(request):
    usuario = Usuario.objects.get(username=request.session["username"])

    if request.method == "GET":
        try:
            clientes = Cliente.objects.filter(id_estado_cliente=1)

            return render(
                request,
                "solicitudes/solicitudes_crear.html",
                {"clientes": clientes, "usuario": usuario},
            )
        except Exception as e:
            print("el error es: ", e)
    else:
        try:
            if usuario.is_staff:
                cliente = Cliente.objects.get(
                    username=request.POST.get("selectCliente")
                )
            else:
                cliente = Cliente.objects.get(username=request.user.username)

            id_estado_solicitud = request.POST.get("id_estado_solicitud", None)

            solicitud = Solicitud.objects.create(
                objetos_a_transportar=request.POST["objetos_a_transportar"],
                detalles=request.POST["detalles"],
                direccion_desde=request.POST["direccion_desde"],
                latitud_desde=request.POST["latitud_desde"],
                longitud_desde=request.POST["longitud_desde"],
                direccion_hasta=request.POST["direccion_hasta"],
                latitud_hasta=request.POST["latitud_hasta"],
                longitud_hasta=request.POST["longitud_hasta"],
                ha_pagado=0,
                devolucion="",
                id_estado_solicitud=EstadosSolicitud.objects.get(
                    id=id_estado_solicitud
                ),
                fecha_trabajo=request.POST["fecha_trabajo"],
                cliente_id=cliente,
            )

            solicitud.save()

            return redirect("solicitudes")
        except Exception as e:
            if e == "Cliente matching query does not exist.":
                print("Error en solicitudes_crear:", e)
                return render(
                    request,
                    "solicitudes/solicitudes_crear.html",
                    {
                        "error": "Usted no se encuentra hablitado para crear una solicitud."
                    },
                )
            else:
                print("Error en solicitudes_crear:", e)
                return render(
                    request,
                    "solicitudes/solicitudes_crear.html",
                    {"error": "No ha sido posible guardar la solicitud."},
                )


@login_required
def solicitud_detalle(request, solicitud_id):
    tipo_usuario = Usuario.objects.get(username=request.user.username)

    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    estados = EstadosSolicitud.objects.all()

    lista_empleados_disponibles = list(Empleado.objects.filter(id_estado_empleado=1))

    lista_empleados_asignados = [
        sel.id_empleado
        for sel in SolicitudesEmpleados.objects.filter(id_solicitud=solicitud_id)
    ]

    lista_vehiculos_disponibles = list(Vehiculo.objects.filter(id_estado_vehiculo=1))

    lista_vehiculos_asignados = [
        sel.id_vehiculo
        for sel in SolicitudesVehiculos.objects.filter(id_solicitud=solicitud_id)
    ]

    if request.method == "GET":
        return render(
            request,
            "solicitudes/solicitud_detalle.html",
            {
                "solicitud": solicitud,
                "estados": estados,
                "lista_empleados_disponibles": lista_empleados_disponibles,
                "lista_empleados_asignados": lista_empleados_asignados,
                "lista_vehiculos_disponibles": lista_vehiculos_disponibles,
                "lista_vehiculos_asignados": lista_vehiculos_asignados,
            },
        )
    elif request.method == "POST":
        form_data = request.POST.copy()
        form_data.pop("csrfmiddlewaretoken", None)

        empleados_asignados = form_data.getlist("empleados")
        vehiculos_asignados = form_data.getlist("vehiculos")

        # 1: Actualizar los datos modificados de la solicitud
        resultado_solicitud = actualizar_solicitud(solicitud, form_data)

        resultado_empleados = True
        resultado_vehiculos = True

        if tipo_usuario.id_tipo_usuario.id != 1:
            # 2: Actualizar los empleados asignados al viaje
            resultado_empleados = actualizar_empleados_asignados(
                solicitud, empleados_asignados
            )

            # 3: Actualizar los vehiculos asignados al viaje
            resultado_vehiculos = actualizar_vehiculos_asignados(
                solicitud, vehiculos_asignados
            )

        if resultado_solicitud and resultado_empleados and resultado_vehiculos:
            return redirect("solicitudes")
        else:
            error = ""
            if resultado_solicitud is False:
                error = "No se pudo actualizar la solicitud"
            elif resultado_empleados is False:
                error = (
                    "No se pudo actualizar la asignacion de empleados a la solicitud"
                )
            elif resultado_vehiculos is False:
                error = (
                    "No se pudo actualizar la asignacion de vehiculos a la solicitud"
                )

            return render(
                request,
                "solicitudes/solicitud_detalle.html",
                {
                    "solicitud": solicitud,
                    "estados": estados,
                    "lista_empleados_disponibles": lista_empleados_disponibles,
                    "lista_empleados_asignados": lista_empleados_asignados,
                    "lista_vehiculos_disponibles": lista_vehiculos_disponibles,
                    "lista_vehiculos_asignados": lista_vehiculos_asignados,
                    "error": error,
                },
            )


@transaction.atomic
def actualizar_solicitud(solicitud, form_data):
    try:
        for campo, nuevo_valor in form_data.items():
            if campo == "id_estado_solicitud":
                nuevo_estado = EstadosSolicitud.objects.get(id=nuevo_valor)
                if solicitud.id_estado_solicitud != nuevo_estado:
                    solicitud.id_estado_solicitud = nuevo_estado
            elif campo == "objetos_a_transportar":
                solicitud.objetos_a_transportar = nuevo_valor
            elif campo == "detalles":
                solicitud.detalles = nuevo_valor
            elif campo == "direccion_desde":
                solicitud.direccion_desde = nuevo_valor
            elif campo == "direccion_hasta":
                solicitud.direccion_hasta = nuevo_valor
            elif campo == "calificacion":
                solicitud.calificacion = nuevo_valor
            elif campo == "devolucion":
                solicitud.devolucion = nuevo_valor
            elif campo == "presupuesto":
                solicitud.presupuesto = nuevo_valor

        solicitud.save()
        return True
    except Exception as e:
        print("Error al actualizar_solicitud", e)
        return False


@transaction.atomic
def actualizar_empleados_asignados(solicitud, lista_empleados_asignados):
    try:
        # Eliminar registros de empleados deseleccionados
        empleados_solicitud = SolicitudesEmpleados.objects.filter(
            id_solicitud=solicitud
        )
        for empleado_relacion in empleados_solicitud:
            if str(empleado_relacion.id_empleado_id) not in lista_empleados_asignados:
                empleado_relacion.delete()

        # Agregar registros para empleados seleccionados
        for empleado_id in lista_empleados_asignados:
            if not SolicitudesEmpleados.objects.filter(
                id_solicitud=solicitud, id_empleado_id=empleado_id
            ).exists():
                empleado_relacion = SolicitudesEmpleados(
                    id_solicitud=solicitud, id_empleado_id=empleado_id
                )
                empleado_relacion.save()

        return True
    except Exception as e:
        print("Error al actualizar asignacion de empleados", e)
        return False


@transaction.atomic
def actualizar_vehiculos_asignados(solicitud, lista_vehiculos_asignados):
    try:
        # Eliminar registros de vehiculos deselecciondos
        vehiculos_solicitud = SolicitudesVehiculos.objects.filter(
            id_solicitud=solicitud
        )
        for vehiculo_relacion in vehiculos_solicitud:
            if str(vehiculo_relacion.id_vehiculo_id) not in lista_vehiculos_asignados:
                vehiculo_relacion.delete()

        # Agregar registros para vehiculos seleccionados
        for vehiculo_id in lista_vehiculos_asignados:
            if not SolicitudesVehiculos.objects.filter(
                id_solicitud=solicitud, id_vehiculo_id=vehiculo_id
            ).exists():
                vehiculo_relacion = SolicitudesVehiculos(
                    id_solicitud=solicitud, id_vehiculo_id=vehiculo_id
                )
                vehiculo_relacion.save()

        return True
    except Exception as e:
        print("Error al actualzar asignacion de vehiculos", e)
        return False


@login_required
def solicitud_eliminar(request, solicitud_id):
    print("eliminando solicitud ...")
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    solicitud.delete()
    print("solicitud eliminada")
    return redirect("solicitudes")


@login_required
def solicitud_calificar(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

    if request.method == "GET":
        return render(
            request,
            "solicitudes/solicitud_calificar.html",
            {"solicitud_id": solicitud_id},
        )
    elif request.method == "POST":
        form_data = request.POST.copy()
        form_data.pop("csrfmiddlewaretoken", None)

        resultado_solicitud = actualizar_solicitud(solicitud, form_data)

        if resultado_solicitud:
            return redirect("solicitudes")
        else:
            error = "No se pudo guardar los datos"

        return render(
            request,
            "solicitudes/solicitud_calificar.html",
            {"solicitud": solicitud, "error": error},
        )


@login_required
def solicitudes_reportes(request):
    resultado = ""

    if request.method == "GET":
        return render(request, "solicitudes/solicitudes_reportes.html")

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            fecha_inicio = data.get("fechaInicio", None)
            fecha_fin = data.get("fechaFin", None)

            if fecha_fin > fecha_inicio:
                resultado = "Las fechas estan bien"
                estados = EstadosSolicitud.objects.all()

                reporte = []
                for estado in estados:
                    cantidad_solicitudes = Solicitud.objects.filter(
                        fecha_trabajo__gte=fecha_inicio,
                        fecha_trabajo__lte=fecha_fin,
                        id_estado_solicitud=estado,
                    ).count()
                    reporte.append(
                        {
                            "descripcion": estado.descripcion,
                            "cantidad": cantidad_solicitudes,
                        }
                    )

                data = {"estados": reporte}
                
            else:
                # return render(
                #     request,
                #     "solicitudes/solicitudes_reportes.html",
                #     {"resultado": "error_fechas"},
                # )
                data = {"error": "Error: La fecha inicial debe ser menor o igual a la fecha final."}

            return JsonResponse(data, safe=False)    

        except json.JSONDecodeError as e:
            return JsonResponse({"error": "Error en los datos JSON"}, status=400)


# VISTAS EMPLEADOS


@login_required
def empleados(request):
    return render(request, "empleados/empleados.html")


def empleados_listado(request):
    try:
        objUsuario = Usuario.objects.get(username=request.session["username"])
        usuario_data = objUsuario.to_dict()

        empleados = Empleado.objects.all()
        empleados_data = [empleado.to_dict() for empleado in empleados]

        data = {"empleados": empleados_data, "usuario": usuario_data}

        return JsonResponse(data, safe=False)

    except Exception as e:
        print("Error en empleados:", e)
        return render(
            request,
            "empleados/empleados.html",
            {"error": "Ha ocurrido un error al listar los empleados"},
        )


@login_required
def empleados_crear(request):
    if request.method == "GET":
        return render(request, "empleados/empleados_crear.html")
    elif request.method == "POST":
        try:

            id_estado_empleado = request.POST.get("id_estado_empleado", None)

            id_tipo_usuario = request.POST.get("id_tipo_usuario", None)

            try:
                isAdmin = 0
                if request.POST["administrativo"] == "true":
                    isAdmin = 1
            except Exception as e:
                isAdmin = 0

            empleado = Empleado.objects.create_user(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                username=request.POST["username"],
                password=request.POST["last_name"] + "-e",
                email=request.POST["email"],
                dni=request.POST["dni"],
                telefono=request.POST["telefono"],
                administrativo=isAdmin,
                fecha_nac=request.POST["fecha_nac"],
                tipo_carnet=request.POST["tipo_carnet"],
                ausencias=0,
                is_staff=1,
                id_estado_empleado=EstadosEmpleado.objects.get(id=id_estado_empleado),
                id_tipo_usuario=TiposUsuario.objects.get(id=id_tipo_usuario),
            )
            empleado.save()
            return redirect("empleados")
        except Exception as e:
            print("Error en empleados_crear:", e)
            return render(
                request,
                "empleados/empleados_crear.html",
                {"error": "Ocurrio un error al registrar el empleado."},
            )


@login_required
def empleado_detalle(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    estados = EstadosEmpleado.objects.all()

    if empleado.administrativo == True:
        empleado.administrativo = 1
    else:
        empleado.administrativo = 0

    if request.method == "GET":
        return render(
            request,
            "empleados/empleado_detalle.html",
            {"empleado": empleado, "estados": estados},
        )

    elif request.method == "POST":
        r_post = request.POST.copy()
        r_post.pop("csrfmiddlewaretoken", None)

        administrativo_value = request.POST.get("administrativo")

        if administrativo_value == None:
            administrativo_value = 0
            r_post.update({"administrativo": administrativo_value})

        resultado = actualizar_empleado(r_post, empleado_id)

        if resultado:
            return redirect("empleados")
        else:
            return redirect("empleados/empleado_detalle.html")


def actualizar_empleado(r_post, empleado_id):
    try:
        empleado = Empleado.objects.get(id=empleado_id)
    except Empleado.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        print(campo, nuevo_valor)
        try:
            if campo == "id_estado_empleado":
                nuevo_estado = EstadosEmpleado.objects.get(id=nuevo_valor)
                if empleado.id_estado_empleado != nuevo_estado:
                    empleado.id_estado_empleado = nuevo_estado

            elif getattr(empleado, campo) != nuevo_valor:
                setattr(empleado, campo, nuevo_valor)
        except Exception as e:
            print("Error en empleado_detalle:", e)

    if any(
        getattr(empleado, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()
    ):
        empleado.save()
    return True


@login_required
def empleado_eliminar(request, empleado_id):
    print("eliminando empleado ...")
    try:
        empleado = get_object_or_404(Empleado, pk=empleado_id)
        print(empleado_id)
        print(empleado)
        empleado.delete()
        print("empleado eliminando !")
    except Exception as e:
        print("Error en empleado_eliminar:", e)

    return redirect("empleados")


@login_required
def empleados_reportes(request):
    if request.method == "GET":
        return render(request, "empleados/empleados_reportes.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            fecha_inicio = data.get("fechaInicio", None)
            fecha_fin = data.get("fechaFin", None)
            listar_por = data.get("listarPor", None)

            if listar_por == "nombres":
                reporte = []

                viajes_por_empleado = Empleado.objects.annotate(
                    cantidad_viajes=Count(
                        "solicitudesempleados__id_solicitud__fecha_trabajo",
                        filter=Q(
                            solicitudesempleados__id_solicitud__fecha_trabajo__range=(
                                fecha_inicio,
                                fecha_fin,
                            )
                        ),
                    )
                )

                reporte = []
                for empleado in viajes_por_empleado:
                    cantidad_solicitudes = empleado.cantidad_viajes
                    reporte.append(
                        {
                            "nombre": f"{empleado.last_name} {empleado.first_name}",
                            "cantidadSolicitudes": cantidad_solicitudes,
                        }
                    )

                data = {
                    "empleados": reporte
                    # empleados.nombre
                    # empleados.cantidadSolicitudes
                }
            elif listar_por == "estados":
                estados = EstadosEmpleado.objects.all()
                reporte = []
                for estado in estados:
                    cantidad_empleados = Empleado.objects.filter(
                        id_estado_empleado=estado
                    ).count()
                    reporte.append(
                        {
                            "descripcion": estado.descripcion,
                            "cantidadEmpleados": cantidad_empleados,
                        }
                    )

                data = {
                    "estados": reporte
                    # estados.descripcion
                    # estados.cantidad
                }

            print(data)
            return JsonResponse(data, safe=False)
        except:
            return JsonResponse({"error": "Error en los datos JSON"}, status=400)


# VISTAS VEHICULOS


@login_required
def vehiculos(request):
    return render(request, "vehiculos/vehiculos.html")


def vehiculos_listado(request):
    try:
        objUsuario = Usuario.objects.get(username=request.session["username"])
        usuario_data = objUsuario.to_dict()

        vehiculos = Vehiculo.objects.all()
        vehiculos_data = [vehiculo.to_dict() for vehiculo in vehiculos]

        data = {"vehiculos": vehiculos_data, "usuario": usuario_data}

        return JsonResponse(data, safe=False)
    except Exception as e:
        print("Error en vehiculos:", e)
        return render(
            request,
            "vehiculos/vehiculos.html",
            {"error": "Ha ocurrido un error al listar los vehiculos"},
        )


@login_required
def vehiculos_crear(request):
    vehiculo = ""
    if request.method == "GET":
        return render(request, "vehiculos/vehiculos_crear.html")
    else:
        try:
            id_estado_vehiculo = request.POST.get("id_estado_vehiculo", None)
            vehiculo = Vehiculo.objects.create(
                dominio=request.POST["dominio"],
                marca=request.POST["marca"],
                nombre=request.POST["nombre"],
                modelo=request.POST["modelo"],
                capacidad=request.POST["capacidad"],
                kilometraje=request.POST["kilometraje"],
                fecha_ult_service=request.POST["fecha_ult_service"],
                id_estado_vehiculo=EstadosVehiculo.objects.get(id=id_estado_vehiculo),
            )

            vehiculo.save()

            return redirect("vehiculos")
        except Exception as e:  # revisar bug
            if e == "UNIQUE constraint failed: solicitudes_vehiculo.dominio":
                print("Error en patente ", e)
                return render(
                    request,
                    "vehiculos/vehiculos_crear.html",
                    {
                        "vehiculo": vehiculo,
                        "error": "El dominio ya pertenece a otro vehiculo registrado",
                    },
                )
            else:
                print("Error en vehiculos_crear: ", e)
                return render(
                    request,
                    "vehiculos/vehiculos_crear.html",
                    {"vehiculo": vehiculo, "error": "No se pudo registrar el vehiculo"},
                )


@login_required
def vehiculo_detalle(request, vehiculo_id):
    if request.method == "GET":
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        estados = EstadosVehiculo.objects.all()

        return render(
            request,
            "vehiculos/vehiculo_detalle.html",
            {"vehiculo": vehiculo, "estados": estados},
        )
    else:  # POST
        if request.POST["fecha_ult_service"] == "":
            r_post = request.POST.copy()
            r_post.pop("csrfmiddlewaretoken", None)
            r_post.pop("fecha_ult_service", None)
        else:
            r_post = request.POST.copy()
            r_post.pop("csrfmiddlewaretoken", None)

        resultado = actualizar_vehiculo(r_post, vehiculo_id)

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
        if request.POST["fecha_ult_service"] != vehiculo.fecha_ult_service:
            vehiculo.fecha_ult_service = request.POST["fecha_ult_service"]

        if resultado:
            return redirect("vehiculos")
        else:
            return render(
                request,
                "vehiculos/vehiculo_detalle.html",
                {"error": "Ha ocurrido un error al actualizar los datos del vehiculo"},
            )


def actualizar_vehiculo(r_post, vehiculo_id):
    try:
        vehiculo = Vehiculo.objects.get(id=vehiculo_id)
    except Vehiculo.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        try:
            if campo == "id_estado_vehiculo":
                nuevo_estado = EstadosVehiculo.objects.get(id=nuevo_valor)
                if vehiculo.id_estado_vehiculo != nuevo_estado:
                    vehiculo.id_estado_vehiculo = nuevo_estado
            elif getattr(vehiculo, campo) != nuevo_valor:
                setattr(vehiculo, campo, nuevo_valor)
        except Exception as e:
            print("Error en actualizar vehiculo: ", e)

    if any(
        getattr(vehiculo, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()
    ):
        vehiculo.save()
    return True


@login_required
def vehiculo_eliminar(request, vehiculo_id):
    print("eliminando vehiculo ...")
    
    try:
        vehiculo = get_object_or_404(Vehiculo, pk=vehiculo_id)
        vehiculo.delete()
        return redirect("vehiculos")
    except Exception as e:
        print("Error en vehiculo_eliminar:", e)


@login_required
def vehiculos_reportes(request):
    if request.method == "GET":
        return render(request, "vehiculos/vehiculos_reportes.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            fecha_inicio = data.get("fechaInicio", None)
            fecha_fin = data.get("fechaFin", None)
            listar_por = data.get("listarPor", None)
            reporte = []

            if listar_por == "estados":
                estados = EstadosVehiculo.objects.all()

                try:
                    for estado in estados:
                        cantidad_vehiculos = Vehiculo.objects.filter(
                            id_estado_vehiculo=estado
                        ).count()
                        reporte.append(
                            {
                                "descripcion": estado.descripcion,
                                "cantidadVehiculos": cantidad_vehiculos,
                            }
                        )

                    data = {"estados": reporte}

                    return JsonResponse(data, safe=False)

                except Exception as e:
                    print("Error en reporte de vehiculos por estados:", e)

            elif listar_por == "vehiculos":
                try:
                    qSolicitudesVehiculos = Vehiculo.objects.annotate(
                        cantidad_viajes=Count(
                            "solicitudesvehiculos__id_solicitud__fecha_trabajo",
                            filter=Q(
                                solicitudesvehiculos__id_solicitud__fecha_trabajo__range=(
                                    fecha_inicio,
                                    fecha_fin,
                                )
                            ),
                        )
                    )
                    for vehiculo in qSolicitudesVehiculos:
                        reporte.append(
                            {
                                "nombreModelo": f"{vehiculo.nombre} {vehiculo.modelo}",
                                "cantidadViajes": vehiculo.cantidad_viajes,
                            }
                        )

                    data = {"vehiculos": reporte}
                except Exception as e:
                    print("Error en reporte de vehiculos por cantidades:", e)

            return JsonResponse(data, safe=False)
        except:
            return JsonResponse({"error": "Error en los datos JSON"}, status=400)


# VISTAS CLIENTES


@login_required
def clientes(request):
    return render(request, "clientes/clientes.html")


def clientes_listado(request):
    try:
        objUsuario = Usuario.objects.get(username=request.session["username"])
        usuario_data = objUsuario.to_dict()
        
        clientes = Cliente.objects.all()
        clientes_data = [cliente.to_dict() for cliente in clientes]

        data = {"clientes": clientes_data, "usuario": usuario_data}
        return JsonResponse(data, safe=False)
    except Exception as e:
        print("Error en empleados:", e)
        return render(
            request,
            "clientes/clientes.html",
            {"error": "Ha ocurrido un error al listar los clientes"},
        )


@login_required
def cliente_detalle(request, cliente_id):
    if request.method == "GET":
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        estados = EstadosCliente.objects.all()

        return render(
            request,
            "clientes/cliente_detalle.html",
            {"cliente": cliente, "estados": estados},
        )
    else:
        r_post = request.POST.copy()
        r_post.pop("csrfmiddlewaretoken", None)
        resultado = actualizar_cliente(r_post, cliente_id)

        if resultado:
            return redirect("clientes")
        else:
            return render(
                request,
                "clientes/cliente_detalle.html",
                {"error": "Ha ocurrido un error al actualizar los datos del cliente"},
            )


def actualizar_cliente(r_post, cliente_id):
    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return False

    for campo, nuevo_valor in r_post.items():
        try:
            if campo == "id_estado_cliente":
                nuevo_estado = EstadosCliente.objects.get(id=nuevo_valor)
                if cliente.id_estado_cliente != nuevo_estado:
                    cliente.id_estado_cliente = nuevo_estado
            elif getattr(cliente, campo) != nuevo_valor:
                setattr(cliente, campo, nuevo_valor)
        except Exception as e:
            print("Error en actualizar cliente: ", e)

    if any(
        getattr(cliente, campo) != nuevo_valor for campo, nuevo_valor in r_post.items()
    ):
        cliente.save()
    return True


@login_required
def cliente_eliminar(request, cliente_id):

    print("eliminando cliente ...")

    try:
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cliente.delete()
        print("cliente eliminado !")
    except Exception as e:
        print("Error en cliente_eliminar:", e)
    return redirect("clientes")


@login_required
def clientes_reportes(request):
    if request.method == "GET":
        return render(request, "clientes/clientes_reportes.html")
    elif request.method == "POST":
        try:
            data = json.loads(request.body)

            print(data)

            fecha_inicio = data.get("fechaInicio", None)
            fecha_fin = data.get("fechaFin", None)
            listar_por = data.get("listarPor", None)
            reporte = []

            if listar_por == "estados":
                estados = EstadosCliente.objects.all()
                for estado in estados:
                    cantidad_clientes = Cliente.objects.filter(
                        id_estado_cliente=estado
                    ).count()
                    reporte.append(
                        {
                            "descripcion": estado.descripcion,
                            "cantidadClientes": cantidad_clientes,
                        }
                    )

                data = {"estados": reporte}

            elif listar_por == "nombres":
                viajes_por_cliente = Cliente.objects.annotate(
                    cantidad_viajes=Count(
                        "solicitud__id",
                        filter=Q(
                            solicitud__fecha_trabajo__range=(fecha_inicio, fecha_fin)
                        ),
                    )
                )
                for cliente in viajes_por_cliente:
                    reporte.append(
                        {
                            "nombre": f"{cliente.last_name} {cliente.first_name}",
                            "cantidadViajes": cliente.cantidad_viajes,
                        }
                    )

                print(reporte)

                data = {"clientes": reporte}

            print(data)

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": e}, status=400)


@login_required
def clientes_crear(request):
    if request.method == "GET":
        return render(request, "clientes/cliente_crear.html")
    elif request.method == "POST":
        try:
            id_estado_cliente = request.POST.get("id_estado_cliente", None)
            id_tipo_usuario = request.POST.get("id_tipo_usuario", None)

            cliente = Cliente.objects.create_user(
                first_name=request.POST["first_name"],
                last_name=request.POST["last_name"],
                username=request.POST["username"],
                password=request.POST["password1"],
                email=request.POST["email"],
                dni=request.POST["dni"],
                telefono=request.POST["telefono"],
                id_estado_cliente=EstadosCliente.objects.get(id=id_estado_cliente),
                id_tipo_usuario=TiposUsuario.objects.get(id=id_tipo_usuario),
                fecha_nac=request.POST["fecha_nac"],
                fecha_creacion=date.today(),
                puntos=0,
            )
            cliente.save()

            return redirect("clientes")
        except Exception as e:
            print("Error en signup:", e)
            return render(
                request,
                "auth/signup.html",
                {"error": "Ocurrio un error al registrar el usuario."},
            )


# VISTAS DE ERROR
def error_view_500(request):
    error_message = "Se ha producido un error interno en el servidor."
    error_details = "Missing staticfiles manifest entry for 'css/styles.css'"
    context = {
        "error_message": error_message,
        "error_details": error_details,
    }
    return render(request, "error_500.html", context, status=500)
