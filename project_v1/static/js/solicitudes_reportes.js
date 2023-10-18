const form_filtros = document.getElementById("form_filtros");
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { className: 'centered', targets: [1, 2] }
    ],
    destroy: true
}

// Inicializacion de la datatable
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listReportes();

    try {
        dataTable = $(`#datatable_Solicitudes`).DataTable({ ...dataTableOptions });
    } catch (ex) {
        alert(ex)
    }

    dataTableIsInitialized = true;
}

// Proceso de informacion 
const listReportes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/solicitudes/reportes');
        const data = await response.json();

        console.log(data.solicitudes)

        let content = '';

        // Estados
        let aPresupuestar = 0;       // 1. A presupuestar
        let presupuestada = 0;       // 2. Presupuestada
        let presupuestoEnviado = 0;  // 3. Presupuesto enviado
        let presupuestoAceptado = 0; // 4. Presupuesto aceptado
        let enCamino = 0;            // 5. En camino
        let entregado = 0;           // 6. Entregado
        let calificado = 0;          // 7. Calificado

        data.solicitudes.forEach((solicitud, index) => {

            switch (solicitud.estado) {
                case 'A presupuestar':
                    aPresupuestar += 1;
                    break;
                case 'Presupuestada':
                    presupuestada += 1;
                    break;
                case 'Presupuesto enviado':
                    presupuestoEnviado += 1;
                    break;
                case 'Presupuesto aceptado':
                    presupuestoAceptado += 1;
                    break;
                case 'En camino':
                    enCamino += 1;
                    break;
                case 'Entregado':
                    entregado += 1;
                    break;
                case 'Calificado':
                    calificado += 1;
                    break;
                default:

            }
        });
        
        content = `
            <tr>
                <th>Estado</th>
                <th>Cantidad</th>
            </tr>
            <tr>
                <td>A presupuestar</td>
                <td>${aPresupuestar}</td>
            </tr>
            <tr>
                <td>Presupuestada</td>
                <td>${presupuestada}</td>
            </tr>
            <tr>
                <td>Presupuesto enviado</td>
                <td>${presupuestoEnviado}</td>
            </tr>
            <tr>
                <td>Presupuesto aceptado</td>
                <td>${presupuestoAceptado}</td>
            </tr>
            <tr>
                <td>En camino</td>
                <td>${enCamino}</td>
            </tr>
            <tr>
                <td>Entregado</td>
                <td>${entregado}</td>
            </tr>
            <tr>
                <td>Calificado</td>
                <td>${calificado}</td>
            </tr>
        `

        tableBody_Solicitudes.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

// Escucha del boton click
form_filtros.addEventListener("click", function (event) {
    event.preventDefault();
})