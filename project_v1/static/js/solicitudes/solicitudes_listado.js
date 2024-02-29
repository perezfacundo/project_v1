// let dataTable;
// let dataTableIsInitialized = false;
// let tableBody = document.getElementById("tableBody");

// let botonTodas = document.getElementById("btnRadioTodas");
// let botonPendientes = document.getElementById("btnRadioPendientes");
// let botonProx7dias = document.getElementById("btnRadioProx7dias");

// let bodyContent = "";
// let btnCalificar = "";
// let btnDetalles = "";
// let btnEliminar = "";

// // Configuracion de la datatable
// const dataTableOptions = {
//   columnDefs: [
//     { className: "centered", targets: [0, 1, 2, 3, 4, 5, 6, 7] },
//     { orderable: false, targets: [5, 6, 7] },
//     { searchable: false, targets: [5, 6, 7] },
//   ],
//   destroy: true,
//   dom: "Bfrtip",
//   buttons: ["copy", "csv", "excel", "pdf", "print"],
// };

// // Inicializacion de la datatable
// const initDataTable = async (listFunction) => {
//   if (dataTableIsInitialized) {
//     if (dataTable) {
//       dataTable.clear();
//     }
//   }

//   await listFunction();

//   try {
//     dataTable = $("#tableSolicitudes").DataTable(dataTableOptions);
//   } catch (ex) {
//     console.error(ex);
//   }

//   dataTableIsInitialized = true;
// };

// botonTodas.addEventListener("click", async () => {
//   await initDataTable(listTodasSolicitudes);
// });

// botonPendientes.addEventListener("click", async () => {
//   await initDataTable(listSolicitudesPendientes);
// });

// botonProx7dias.addEventListener("click", async () => {
//   await initDataTable(listSolicitudesProx7dias);
// });

// // Proceso de informacion
// const listTodasSolicitudes = async () => {
//   bodyContent = "";
//   btnCalificar = "";
//   btnDetalles = "";
//   btnEliminar = "";

//   try {
//     const response = await fetch("http://127.0.0.1:8000/solicitudes_listado/");
//     const data = await response.json();
//     const usuario = data.usuario;
//     const solicitudes = data.solicitudes;

//     console.log("Listado de todas las solicitudes");
//     console.log(data);

//     solicitudes.forEach((solicitud) => {
//       btnCalificar = `<a class="btn btn-sm " style="background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
//       btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
//       btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

//       bodyContent += `
//                     <tr>
//                         <td>${solicitud.id}</td>
//                         <td>${solicitud.cliente}</td>
//                         <td>${solicitud.direccion_desde}</td>
//                         <td>${solicitud.direccion_hasta}</td>
//                         <td>${solicitud.fecha_trabajo}</td>
//                         <td>${solicitud.estado}</td>
//                         <td>${btnDetalles}
//         `;

//       if (usuario.tipo_usuario == "Administrador") {
//         bodyContent += `${btnEliminar}`;
//       }

//       if (solicitud.estado == "Entregado") {
//         if (usuario.tipo_usuario == "Cliente") {
//           bodyContent += `${btnCalificar}`;
//         }
//       }

//       bodyContent += `</td><td>`;
//       if (solicitud.calificacion != null) {
//         for (var i = 1; i <= solicitud.calificacion; i++) {
//           bodyContent += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
//         }
//       } else {
//         bodyContent += `sin calificar`;
//       }
//       bodyContent += `</td></tr>`;
//     });

//     tableBody.innerHTML = bodyContent;
//   } catch (error) {
//     alert(error);
//   }
//   tableBody.innerHTML = bodyContent;
//   updateDataTable();
// };

// const listSolicitudesPendientes = async () => {
//   bodyContent = "";
//   btnCalificar = "";
//   btnDetalles = "";
//   btnEliminar = "";

//   try {
//     const response = await fetch(
//       "http://127.0.0.1:8000/solicitudes_pendientes/"
//     );
//     const data = await response.json();
//     const usuario = data.usuario;
//     const solicitudes = data.solicitudes;

//     console.log("Listado de solicitudes pendientes");
//     console.log(data);

//     solicitudes.forEach((solicitud) => {
//       btnCalificar = `<a class="btn btn-sm " style="background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
//       btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
//       btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

//       bodyContent += `
//                     <tr>
//                         <td>${solicitud.id}</td>
//                         <td>${solicitud.cliente}</td>
//                         <td>${solicitud.direccion_desde}</td>
//                         <td>${solicitud.direccion_hasta}</td>
//                         <td>${solicitud.fecha_trabajo}</td>
//                         <td>${solicitud.estado}</td>
//                         <td>${btnDetalles}
//         `;

//       if (usuario.tipo_usuario == "Administrador") {
//         bodyContent += `${btnEliminar}`;
//       }

//       if (solicitud.estado == "Entregado") {
//         if (usuario.tipo_usuario == "Cliente") {
//           bodyContent += `${btnCalificar}`;
//         }
//       }

//       bodyContent += `</td><td>`;
//       if (solicitud.calificacion != null) {
//         for (var i = 1; i <= solicitud.calificacion; i++) {
//           bodyContent += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
//         }
//       } else {
//         bodyContent += `sin calificar`;
//       }
//       bodyContent += `</td></tr>`;
//     });
//   } catch (error) {
//     alert(error);
//   }
//   tableBody.innerHTML = bodyContent;
//   updateDataTable();
// };

// const listSolicitudesProx7dias = async () => {
//   bodyContent = "";
//   btnCalificar = "";
//   btnDetalles = "";
//   btnEliminar = "";

//   try {
//     const response = await fetch(
//       "http://127.0.0.1:8000/solicitudes_prox7dias/"
//     );
//     const data = await response.json();
//     const usuario = data.usuario;
//     const solicitudes = data.solicitudes;

//     console.log("Listado de solicitudes en los proximos 7 dias");
//     console.log(data);

//     solicitudes.forEach((solicitud) => {
//       btnCalificar = `<a class="btn btn-sm " style="background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
//       btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
//       btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

//       bodyContent += `
//                     <tr>
//                         <td>${solicitud.id}</td>
//                         <td>${solicitud.cliente}</td>
//                         <td>${solicitud.direccion_desde}</td>
//                         <td>${solicitud.direccion_hasta}</td>
//                         <td>${solicitud.fecha_trabajo}</td>
//                         <td>${solicitud.estado}</td>
//                         <td>${btnDetalles}
//         `;

//       if (usuario.tipo_usuario == "Administrador") {
//         bodyContent += `${btnEliminar}`;
//       }

//       if (solicitud.estado == "Entregado") {
//         if (usuario.tipo_usuario == "Cliente") {
//           bodyContent += `${btnCalificar}`;
//         }
//       }

//       bodyContent += `</td><td>`;
//       if (solicitud.calificacion != null) {
//         for (var i = 1; i <= solicitud.calificacion; i++) {
//           bodyContent += `<i class="bi bi-star-fill" style="color:#F8DA62;"></i>`;
//         }
//       } else {
//         bodyContent += `sin calificar`;
//       }
//       bodyContent += `</td></tr>`;
//     });
//   } catch (error) {
//     alert("ERROR EN listar solicitudes de los proximos 7 dias:" + error);
//   }

//   tableBody.innerHTML = bodyContent;
//   updateDataTable();
// };

// // Función para actualizar DataTable después de cambiar el contenido
// const updateDataTable = () => {
//   if (dataTableIsInitialized) {
//     // Comparamos los nuevos datos con los datos existentes
//     const newBodyContent = document.getElementById("bodyContent").innerHTML;
//     const oldBodyContent = dataTable.rows().data();
//     if (newBodyContent !== oldBodyContent) {
//       // Los datos son diferentes, por lo que destruimos la tabla
//       dataTable.clear().destroy();
//     }
//   }

//   // Inicializamos la tabla con los nuevos datos
//   dataTable = $("#tableSolicitudes").DataTable(dataTableOptions);
//   dataTableIsInitialized = true;
// };

// // Escucha del evento load
// window.addEventListener("load", async () => {
//   await initDataTable(listTodasSolicitudes);
// });

// $.post("http://127.0.0.1:8000/solicitudes_listado/", config)
//   .then((response) => {

//   })

let response = "";
let data = "";
let usuario = "";
let solicitudes = "";

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
    let estrellas = "";
    let botonesAccion = "";
    let table = $("#tableSolicitudes").DataTable();
    table.clear().draw();

    solicitudes.forEach((solicitud) => {
      //botones de accion
      btnCalificar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
      btnDetalles = `<a class="btn btn-sm " style="margin:0 3px; background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
      btnEliminar = `<a class="btn btn-sm " style="margin:0 3px; background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

      botonesAccion = `${btnDetalles}`
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
