let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        { orderable: false, targets: [1] },
        { searchable: false, targets: [1] }
    ],
    destroy: true,
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ]
};

// Función para inicializar la DataTable
const initDataTable = async () => {
    try {
        if (dataTableIsInitialized) {
            dataTable.destroy()
        };

        await listReportes();

        dataTable = $('#tableBody_Solicitudes').DataTable(dataTableOptions);

        dataTableIsInitialized = true;
    } catch (ex) {
        alert(ex)
    };
};

const listReportes = async () => {
    try {
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
                    console.log(data.reporte);

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

                    data.reporte.forEach((estado, index) => {
                        console.log(estado)
                    });
                    

                    $('#tableBody_Solicitudes').html(content);
                },

                error: function (error) {
                    console.log('Error: ', error)
                }
            });
        });
    } catch (ex) {
        alert(ex);
    };
};

window.addEventListener("load", async () => {
    await initDataTable();
});
