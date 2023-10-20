let dataTable;
let dataTableIsInitialized = false;

// Configuracion de la datatable
const dataTableOptions = {
    columnDefs: [
        { className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6] },
        { orderable: false, targets: [4, 5, 6] }
    ],
    destroy: true
}

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listReportes();

    try {
        dataTable = $(`#dataTable_Solicitudes`).DataTable({ ...dataTableOptions })
    } catch (ex) {
        alert(ex)
    }
    dataTableIsInitialized = true;
}


const listReportes = async () => {
    $('#enviarButton').click(function () {
        const fechaInicio = $('#fechaInicio').val();
        const fechaFin = $('#fechaFin').val();
        const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

        const datos = {
            fechaInicio: fechaInicio,
            fechaFin: fechaFin,
            csrfmiddlewaretoken: csrfToken
        };

        $.ajax({
            url: 'http://127.0.0.1:8000/solicitudes/reportes/',
            type: 'POST',
            data: JSON.stringify(datos),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrfToken
            },
            success: function (data) {
                //Proceso de la informacion
                console.log(data.solicitudes);

                let content = '';

                // Estados
                let aPresupuestar = 0;       // 1. A presupuestar
                let presupuestada = 0;       // 2. Presupuestada
                let presupuestoEnviado = 0;  // 3. Presupuesto enviado
                let presupuestoAceptado = 0; // 4. Presupuesto aceptado
                let enCamino = 0;            // 5. En camino
                let entregado = 0;           // 6. Entregado
                let calificado = 0;          // 7. Calificado
                let total = 0;

                data.solicitudes.forEach((solicitud, index) => {
                    total += 1;
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
                            break;
                    }

                    console.log(calificado, presupuestada)

                    content = `
                        <thead>
                            <tr>
                                <th class="centered">Estado</th>
                                <th class="centered">Cantidad</th>
                            </tr>
                        </thead>
                        <tbody>
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
                            <tr>
                                <td><strong>Total</strong></td>
                                <td>${total}</td>
                            </tr>
                        </tbody>
                        <caption>Reporte de solicitudes</caption>
                        `

                    datatable_Solicitudes.innerHTML = content;
                });
            },

            error: function (error) {
                console.error('Error: ', error)
            }
        });
    });
}

$(document).ready(async function () {
    await initDataTable();
});