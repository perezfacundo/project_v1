let dataTable;
let dataTableIsInitialized = false;

let aEmpleados = []
let aCantidades = []

let chart = {
    'tooltip': {
        'show': true,
        'trigger': "axis",
        'triggerOn': "mousemove|click"
    },
    'xAxis': [
        {
            'type': "category",
            'data': aEmpleados
        }
    ],
    'yAxis': [
        {
            'type': "value"
        }
    ],
    'series': [
        {
            'data': aCantidades,
            'type': "bar"
        }
    ]
}

const dataTableOptions = {
    columnDefs: [
        { orderable: false, targets: [1] },
    ],
    "searching": false,
    dom: 'Bfrtip',
    buttons: [
        'copy', 'csv', 'excel', 'pdf', 'print'
    ]
};

// Función para inicializar la DataTable
const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    };

    await listReportes();

    dataTable = $('#table').DataTable(dataTableOptions);

    dataTableIsInitialized = true;
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
                url: 'http://127.0.0.1:8000/empleados/reportes/',
                type: 'POST',
                data: JSON.stringify(datos),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {
                    //Proceso de la informacion

                    let content = '';

                    data.reporte.forEach((estado, index) => {
                        content += `
                            <tr>
                                <td>${estado.descripcion}</td>
                                <td class="centered">${estado.cantidad}</td>
                            </tr>
                        `;
                        aEmpleados.push()
                        aCantidades.push()
                    });

                    tablebody.innerHTML = content;

                    console.log(aEmpleados, aCantidades)
                },
                error: function (error) {
                    console.log('Error: ', error)
                }
            });
        });
    } catch (ex) {
        alert(ex);
        console.log("Error: ", ex)
    };
};

const initChart = async () => {
    try {
        const myChart = echarts.init(document.getElementById("chart"));
        myChart.setOption(chart);
        myChart.resize();
    } catch (ex) {
        alert(ex);
        console.log("Error: ", ex)
    }
}

window.addEventListener("load", async () => {
    await initDataTable();
    await initChart();
});
