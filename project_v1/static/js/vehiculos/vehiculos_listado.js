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
        dataTable = $('#datatable_Vehiculos').DataTable(dataTableOptions);
    } catch (ex) {
        alert(ex)
    }

    dataTableIsInitialized = true;
}

// Proceso de informacion 
const listSolicitudes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/vehiculos_listado/');
        const data = await response.json();

        console.log(data.vehiculos)

        let content = '';
        let btnDetalles = '';
        let btnEliminar = '';

        data.vehiculos.forEach((vehiculo) => {

            btnDetalles = `<a class="btn btn-sm " style="background-color:#357266;" href="http://127.0.0.1:8000/vehiculos/${vehiculo.id}/"><i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i></a>`;
            btnEliminar = `<a class="btn btn-sm " style="background-color:#C44558;" href="http://127.0.0.1:8000/vehiculos/eliminar/${vehiculo.id}"/><i class="bi bi-trash-fill" style="color:#FFFFFF"></i></a>`;

            content += `
                <tr>
                    <td>${vehiculo.id}</td>
                    <td>${vehiculo.nombre} ${vehiculo.modelo}</td>
                    <td>${vehiculo.marca}</td>
                    <td>${vehiculo.dominio}</td>
                    <td>${vehiculo.cantidadViajes}</td>
                    <td>${vehiculo.estado}</td>
                    <td>${btnDetalles} ${btnEliminar}</td>
                </tr>    
            `
        });

        tableBody_Vehiculos.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};


// Escucha del evento load
window.addEventListener('load', async () => {
    await initDataTable();
})