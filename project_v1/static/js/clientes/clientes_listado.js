const dataTableOptions = {
  ordering: true,
  searching: true,
  destroy: true,
  dom: "Bfrtip",
  buttons: ["copy", "csv", "excel", "pdf", "print"],
};

const listClientes = async () => {
  fetch("http://127.0.0.1:8000/clientes_listado/", {
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
    let clientes = respuestaJSON.clientes;
    let usuario = respuestaJSON.usuario;
    console.log(respuestaJSON)
    let table = $("#tableClientes").DataTable(dataTableOptions);
    table.clear().draw();

    clientes.forEach((cliente) => {
      //botones de accion
      let botonesAccion= "";

      btnDetalles = `<a class="btn btn-sm" style="margin-right:2px; background-color:#357266;" href="http://127.0.0.1:8000/clientes/${cliente.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
      btnEliminar = `<a class="btn btn-sm" style="margin-right:2px; background-color:#C44558;" href="http://127.0.0.1:8000/clientes/${cliente.id}/eliminar/"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

      botonesAccion += btnDetalles;
      if (usuario.tipo_usuario === "Administrador") {
        botonesAccion += btnEliminar;
      }

      table.row.add([
        cliente.dni,
        cliente.last_name,
        cliente.first_name,
        cliente.telefono,
        cliente.email,
        cliente.estado,
        botonesAccion
      ]).draw()
    });
  })
  .catch(function (error) {
    console.log("error:", error);
  })
};

window.addEventListener("load", async () => {
  await listClientes();
})