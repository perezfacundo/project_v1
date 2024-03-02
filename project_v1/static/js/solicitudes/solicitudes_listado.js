let botonTodas = document.getElementById("btnRadioTodas");
let botonPendientes = document.getElementById("btnRadioPendientes");
let botonProx7dias = document.getElementById("btnRadioProx7dias");

const dataTableOptions = {
  columnDefs: [
    { className: "centered", targets: [4] },
    { orderable: false, targets: [4, 6, 7] },
    { searchable: false, targets: [4, 5, 6, 7] },
  ],
  destroy: true,
  dom: "Bfrtip",
  buttons: ["copy", "csv", "excel", "pdf", "print"],
};

window.addEventListener("load", async () => {
  await listTodasSolicitudes();
});

botonTodas.addEventListener("click", async () => {
  await listTodasSolicitudes();
});

botonPendientes.addEventListener("click", async () => {
  await listSolicitudesPendientes();
});

botonProx7dias.addEventListener("click", async () => {
  await listSolicitudesProx7dias();
});

const listTodasSolicitudes = async () => {
  fetch("http://127.0.0.1:8000/solicitudes_listado/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Error al obtener la respuesta del servidor");
      }
    })
    .then(function (respuestaJSON) {
      let solicitudes = respuestaJSON.solicitudes;
      let usuario = respuestaJSON.usuario;

      let table = $("#tableSolicitudes").DataTable(dataTableOptions);
      table.clear().draw();

      solicitudes.forEach((solicitud) => {
        let estrellas = "";

        //botones de accion
        let botonesAccion = "";

        btnCalificar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
        btnDetalles = `<a class="btn btn-sm " style="margin:0 3px; background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
        btnEliminar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

        botonesAccion = `${btnDetalles}`;
        if (usuario.tipo_usuario == "Administrador") {
          botonesAccion += `${btnEliminar}`;
        }

        if (solicitud.estado == "Entregado") {
          if (usuario.tipo_usuario == "Cliente") {
            botonesAccion += `${btnCalificar}`;
          }
        }

        //calificacion
        estrellas = "";
        if (solicitud.calificacion != null) {
          for (var i = 1; i <= solicitud.calificacion; i++) {
            estrellas += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
          }
        } else {
          estrellas += `sin calificar`;
        }

        table.row
          .add([
            solicitud.id,
            solicitud.cliente,
            solicitud.direccion_desde,
            solicitud.direccion_hasta,
            solicitud.fecha_trabajo,
            solicitud.estado,
            botonesAccion,
            estrellas,
          ])
          .draw();
      });
    })
    .catch(function (error) {
      console.log("error:", error);
    });
};

const listSolicitudesPendientes = async () => {
  fetch("http://127.0.0.1:8000/solicitudes_pendientes/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Error al obtener la respuesta del servidor");
      }
    })
    .then(function (respuestaJSON) {
      let solicitudes = respuestaJSON.solicitudes;
      let usuario = respuestaJSON.usuario;
      let estrellas = "";
      let botonesAccion = "";
      let table = $("#tableSolicitudes").DataTable();
      table.clear().draw();

      solicitudes.forEach((solicitud) => {
        //botones de accion
        btnCalificar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
        btnDetalles = `<a class="btn btn-sm " style="margin:0 3px; background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
        btnEliminar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

        botonesAccion = `${btnDetalles}`;
        if (usuario.tipo_usuario == "Administrador") {
          botonesAccion += `${btnEliminar}`;
        }

        if (solicitud.estado == "Entregado") {
          if (usuario.tipo_usuario == "Cliente") {
            botonesAccion += `${btnCalificar}`;
          }
        }

        //calificacion
        estrellas = "";
        if (solicitud.calificacion != null) {
          for (var i = 1; i <= solicitud.calificacion; i++) {
            estrellas += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
          }
        } else {
          estrellas += `sin calificar`;
        }

        table.row
          .add([
            solicitud.id,
            solicitud.cliente,
            solicitud.direccion_desde,
            solicitud.direccion_hasta,
            solicitud.fecha_trabajo,
            solicitud.estado,
            botonesAccion,
            estrellas,
          ])
          .draw();
      });
    })
    .catch(function (error) {
      console.log("error:", error);
    });
};

const listSolicitudesProx7dias = async () => {
  fetch("http://127.0.0.1:8000/solicitudes_prox7dias/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Error al obtener la respuesta del servidor");
      }
    })
    .then(function (respuestaJSON) {
      let solicitudes = respuestaJSON.solicitudes;
      let usuario = respuestaJSON.usuario;
      let estrellas = "";
      let botonesAccion = "";
      let table = $("#tableSolicitudes").DataTable();
      table.clear().draw();

      solicitudes.forEach((solicitud) => {
        //botones de accion
        btnCalificar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
        btnDetalles = `<a class="btn btn-sm " style="margin:0 3px; background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
        btnEliminar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

        botonesAccion = `${btnDetalles}`;
        if (usuario.tipo_usuario == "Administrador") {
          botonesAccion += `${btnEliminar}`;
        }

        if (solicitud.estado == "Entregado") {
          if (usuario.tipo_usuario == "Cliente") {
            botonesAccion += `${btnCalificar}`;
          }
        }

        //calificacion
        estrellas = "";
        if (solicitud.calificacion != null) {
          for (var i = 1; i <= solicitud.calificacion; i++) {
            estrellas += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
          }
        } else {
          estrellas += `sin calificar`;
        }

        table.row
          .add([
            solicitud.id,
            solicitud.cliente,
            solicitud.direccion_desde,
            solicitud.direccion_hasta,
            solicitud.fecha_trabajo,
            solicitud.estado,
            botonesAccion,
            estrellas,
          ])
          .draw();
      });
    })
    .catch(function (error) {
      console.log("error:", error);
    });
};
