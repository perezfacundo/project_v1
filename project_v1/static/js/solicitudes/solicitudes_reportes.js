let dataTable;
let dataTableIsInitialized = false;

let arrayEjeX = []
let arrayEjeY = []

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
            'data': arrayEjeX,
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
            'data': arrayEjeY,
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
        dataTable = $('#tableSolicitudes').DataTable(dataTableOptions)
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

            const url = 'http://127.0.0.1:8000/solicitudes/reportes/'

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                // csrfmiddlewaretoken: csrfToken
            };

            const config = {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            }

            fetch(url, config)
                .then(response => response.json())
                .then(data => {
                    let bodyContent = "";
                    let total = 0;

                    data.estados.forEach((estado) => {
                        total += estado.cantidad

                        bodyContent += `
                            <tr>
                                <td>${estado.descripcion}</td>
                                <td>${estado.cantidad}</td>
                            </tr>
                        `;

                        arrayEjeX.push(estado.descripcion)
                        arrayEjeY.push(estado.cantidad)
                    })

                    bodyContent += `
                        <tr>
                            <td><strong>Total</strong></td>
                            <td>${total}</td>
                        </tr>
                    `

                    tableBody.innerHTML = bodyContent;

                    initChart();

                    reiniciarOption();
                })
                .catch(error => console.error('Error:', error))
        });
    } catch (ex) {
        alert(ex);
        console.log("Error: ", ex)
    };
};

window.addEventListener("load", async () => {
    await initDataTable();
});

const initChart = () => {
    let myChart = echarts.init(document.getElementById("chart"));
    myChart.clear();
    myChart.setOption(option);
}

function reiniciarOption() {
    arrayEjeX.splice(0, arrayEjeX.length);
    arrayEjeY.splice(0, arrayEjeY.length);
}