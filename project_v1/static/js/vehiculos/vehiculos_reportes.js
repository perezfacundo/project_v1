let dataTable;
let dataTableIsInitialized = false;
const myChart = echarts.init(document.getElementById("chart"));

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
            'data': aVehiculos,
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

            const url ='http://127.0.0.1:8000/solicitudes/reportes/';

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                // csrfmiddlewaretoken: csrfToken -> para ajax
            };

            const opciones = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            }

            fetch(url, opciones)
                .then(response => response.json())
                .then(data => console.log(data))
                .catch(error => console.error('Error:', error))


            //intentar consulta con fetch para que funcione la tabla 
            $.ajax({
                url: 'http://127.0.0.1:8000/vehiculos/reportes/',
                type: 'POST',
                data: JSON.stringify(datos),
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {

                    let content = '';
                    let total = 0;

                    data.reporte.forEach((vehiculo, index) => {
                        total += vehiculo.cantidad;
                        content += `
                            <tr>
                                <td>${vehiculo.estado}</td>
                                <td class="centered">${vehiculo.cantidadViajes}</td>
                            </tr>
                        `;
                        aVehiculos.push(estado.descripcion)
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
