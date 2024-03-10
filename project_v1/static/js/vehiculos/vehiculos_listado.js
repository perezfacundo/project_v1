const dataTableOptions = {
  columnDefs: [
    // { className: "centered", targets: [4] },
    // { orderable: false, targets: [4, 6, 7] },
    // { searchable: false, targets: [4, 5, 6, 7] },
  ],
  destroy: true,
  dom: "Bfrtip",
  buttons: ["copy", "csv", "excel", "pdf", "print"],
};

const listVehiculos = async () => {
  fetch("http://127.0.0.1:8000/vehiculos_listado/", {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then(function (response) {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Error al obtener una respuesta del servidor");
      }
    })
    .then(function (respuestaJSON) {
      let vehiculos = respuestaJSON.vehiculos;
      let usuario = respuestaJSON.usuario;

      let table = $("#tableVehiculos").DataTable(dataTableOptions);
      table.clear().draw();

      vehiculos.forEach((vehiculo) => {
        let botonesAccion = "";
        let nombre_y_modelo = vehiculo.nombre + " " + vehiculo.modelo

        btnDetalles = `<a class="btn btn-sm" style="margin-right:2px; background-color:#357266;" href="http://127.0.0.1:8000/vehiculos/${vehiculo.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
        btnEliminar = `<a class="btn btn-sm" style="margin-right:2px; background-color:#C44558;" href="http://127.0.0.1:8000/vehiculos/${vehiculo.id}/eliminar/"><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

        botonesAccion += btnDetalles;
        if (usuario.tipo_usuario === "Administrador") {
          botonesAccion += btnEliminar;
        }
        
        table.row.add([
            vehiculo.id,
            nombre_y_modelo,
            vehiculo.marca,
            vehiculo.dominio,
            vehiculo.fecha_ult_service,
            vehiculo.kilometraje,
            vehiculo.estado,
            botonesAccion
        ]).draw();
      });
    })
    .catch(function (error) {
        console.log("error:", error);
    })
};

window.addEventListener("load", async () => {
  await listVehiculos();
});

