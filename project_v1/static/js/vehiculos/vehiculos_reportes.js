let dataTable;
let dataTableIsInitialized = false;
const myChart = echarts.init(document.getElementById("chart"));

const url ='http://127.0.0.1:8000/solicitudes/reportes/';

let aEstados = []
let aCantidades = []

let option = {
    'tooltip': {
        'show': true,
        'trigger': "axis",
        'triggerOn': "mousemove|click"
    },
    'toolbox': {
        'feature': {
          'saveAsImage': { show: true }
        }
    },
    'xAxis': [
        {
            'type': "category",
            'data': aEstados,
            'axisLabel': {
                rotate: 30
            }
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
        if (dataTable) {
            dataTable.destroy();
        }
    };

    await listReportes();

    try {
        dataTable = $('#datatable_Solicitudes').DataTable(dataTableOptions);
    } catch (error) {
        alert(ex)
    }

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

            //intentar consulta con fetch para que funcione la tabla 
            $.ajax({
                url: 'http://127.0.0.1:8000/solicitudes/reportes/',
                type: 'POST',
                data: JSON.stringify(datos),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {

                    let content = '';
                    let total = 0;

                    data.reporte.forEach((estado, index) => {
                        total += estado.cantidad;
                        content += `
                            <tr>
                                <td>${estado.descripcion}</td>
                                <td class="centered">${estado.cantidad}</td>
                            </tr>
                        `;
                        aEstados.push(estado.descripcion)
                        aCantidades.push(estado.cantidad)
                    });

                    content += `
                        <tr>
                            <td><strong>Total</strong></td>
                            <td class="centered">${total}</td>
                        </tr>
                    `

                    tableBody_Solicitudes.innerHTML = content;

                    myChart.setOption(option);
                    myChart.resize();
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

window.addEventListener("load", async () => {
    await initDataTable();
});
