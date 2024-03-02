// let dataTable;
// let dataTableIsInitialized = false;

// // Configuracion de la datatable
// const dataTableOptions = {
//     columnDefs: [
//         { className: 'centered', targets: [4] },
//         { orderable: false, targets: [4, 6, 7] },
//         { searchable: false, targets: [4, 5, 6, 7] }
//     ],
//     destroy: true,
//     dom: 'Bfrtip',
//     buttons: [
//         'copy', 'csv', 'excel', 'pdf', 'print'
//     ]
// }

// // Inicializacion de la datatable
// const initDataTable = async () => {
//     if (dataTableIsInitialized) {
//         if (dataTable) {
//             dataTable.destroy();
//         }
//     }
//     await listEmpleados();

//     try {
//         dataTable = $('#datatable_Empleados').DataTable(dataTableOptions);
//     } catch (ex) {
//         alert(ex)
//     }

//     dataTableIsInitialized = true;
// }

// // Proceso de informacion
// const listEmpleados = async () => {
//     try {
//         const response = await fetch('http://127.0.0.1:8000/empleados_listado/');
//         const data = await response.json();
//         const empleados = data.empleados
//         const usuario = data.usuario

//         let content = '';

//         empleados.forEach((empleado, index) => {
//             btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/empleados/${empleado.id}/"><i class="bi bi-pencil-fill" style="color:#FFFFFF"></i></a>`;
//             btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/empleados/${empleado.id}/eliminar"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

//             content += `
//                 <tr>
//                     <td>${empleado.id}</td>
//                     <td>${empleado.last_name}</td>
//                     <td>${empleado.first_name}</td>
//                     <td>${empleado.last_login}</td>
//                     <td>${empleado.telefono}</td>
//                     <td>${empleado.ausencias}</td>
//                     <td>${empleado.estado}</td>
//                     <td>${btnDetalles}
//             `

//             if(usuario.tipo_usuario == 'Administrador'){
//                 content += `
//                     ${btnEliminar}
//                 `
//             }

//             content += `
//             </td></tr>
//             `

//         });

//         tableBody_Empleados.innerHTML = content;
//     } catch (ex) {
//         alert(ex);
//     }
// };

// // Escucha del evento load
// window.addEventListener('load', async () => {
//     await initDataTable();
// })

//SOLUCION PROBLEMA EXPORTACION

// Configuracion de la datatable
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

const listEmpleados = async () => {
  fetch("http://127.0.0.1:8000/empleados_listado/", {
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
      let empleados = respuestaJSON.empleados;
      let usuario = respuestaJSON.usuario;
      let table = $("#tableEmpleados").DataTable(dataTableOptions);
      table.clear().draw();

      empleados.forEach((empleado) => {
        //botones de accion
        let botonesAccion = ""

        btnDetalles = `<a class="btn btn-sm " style="margin-right:2px; background-color:#357266;" href="http://127.0.0.1:8000/empleados/${empleado.id}/"><i class="bi bi-pencil-fill" style="color:#FFFFFF"></i></a>`;
        btnEliminar = `<a class="btn btn-sm " style="margin-right:2px; background-color:#C44558;" href="http://127.0.0.1:8000/empleados/${empleado.id}/eliminar"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

        botonesAccion += btnDetalles;
        if (usuario.tipo_usuario === "Administrador") {
            botonesAccion += btnEliminar
        }

        table.row.add([
          empleado.id,
          empleado.last_name,
          empleado.first_name,
          empleado.last_login,
          empleado.telefono,
          empleado.ausencias,
          empleado.estado,
        ]).draw();
      });
    })
    .catch(function (error) {
        console.log("error:", error);
    });
};
