let dataTable;
let dataTableIsInitialized = false;

// Configuracion de la datatable
const dataTableOptions = {
    columnDefs: [
        { className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [4, 5, 6] },
        { searchable: false, targets: [4, 5, 6] }
    ],
    destroy: true,
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ]
}

// Inicializacion de la datatable
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        if (dataTable) {
            dataTable.destroy();
        }
    }
    await listSolicitudes();

    try {
        dataTable = $('#datatable_Solicitudes').DataTable(dataTableOptions);
    } catch (ex) {
        alert(ex)
    }

    dataTableIsInitialized = true;
}

// Proceso de informacion 
const listSolicitudes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/solicitudes_listado/');
        const data = await response.json();
        const estados = data.estados
        const usuario = data.usuario

        console.log(data.usuario)

        let content = '';
        let btnCalificar = '';
        let btnDetalles = '';
        let btnEliminar = '';

        data.solicitudes.forEach((solicitud, index) => {
            btnCalificar = `<a class="btn btn-sm " style="background-color:#3B4C7D;" href="http://127.0.0.1:8000/solicitudes/calificar/${solicitud.id}/"><i class="bi bi-star-fill" style="color:#FFFFFF"></i></a>`;
            btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/solicitudes/${solicitud.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
            btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/solicitudes/eliminar/${solicitud.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;
            
            content += `
                <tr>
                    <td>${solicitud.id}</td>
                    <td>${solicitud.direccion_desde}</td>
                    <td>${solicitud.direccion_hasta}</td>
                    <td>${solicitud.fecha_trabajo}</td>
                    <td>${solicitud.estado}</td>
                    <td>${btnDetalles}`

            if (solicitud.estado == "Entregado") {
                if (usuario.tipo_usuario == "Cliente") {
                    content += `${btnCalificar}`
                }
            }

            content += `</td><td>`;
            if (solicitud.calificacion != null) {
                for (var i = 1; i <= solicitud.calificacion; i++) {
                    content += `
                        <i class="bi bi-star-fill" style="color:#F8DA62;"></i>
                    `
                }
            } else { content += `sin calificar` } content += `</td></tr>`
        });

        tableBody_Solicitudes.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};


// Escucha del evento load
window.addEventListener('load', async () => {
    await initDataTable();
})