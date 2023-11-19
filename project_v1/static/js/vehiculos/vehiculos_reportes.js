let dataTable;
let dataTableIsInitialized = false;

var myChart = echarts.init(document.getElementById("chart"));

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
            const listarPor = $('#listarPor').val()

            const url = 'http://127.0.0.1:8000/vehiculos/reportes/';

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                listarPor: listarPor
            };

            const opciones = {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            }

            fetch(url, opciones)
                .then(response => response.json())
                .then(data => {
                    let headContent = "";
                    let bodyContent = "";
                    let total = 0;

                    myChart.clear()

                    if (listarPor === 'vehiculos') {
                        headContent = `
                            <tr>
                                <th class="centered">Vehiculo</th>
                                <th class="centered">Cantidad</th>
                            </tr>
                        `
                        tableHead.innerHTML = headContent;

                        data.vehiculos.forEach((vehiculo) => {
                            total += vehiculo.cantidadViajes;

                            console.log(vehiculo.nombreModelo)
                            console.log(vehiculo.cantidadViajes)

                            bodyContent += `
                                <tr>
                                    <td>${vehiculo.nombreModelo}</td>
                                    <td class="centered">${vehiculo.cantidadViajes}</td>
                                </tr>
                            `;

                            arrayEjeX.push(vehiculo.nombreModelo)
                            arrayEjeY.push(vehiculo.cantidadViajes)
                        });

                    } else if (listarPor === 'estados') {

                        headContent = `
                            <tr>
                                <th class="centered">Estado</th>
                                <th class="centered">Cantidad</th>
                            </tr>
                        `
                        tableHead.innerHTML = headContent;

                        data.estados.forEach((estado) => {
                            total += estado.cantidadVehiculos;

                            console.log(estado.Descripcion)
                            console.log(estado.cantidadVehiculos)

                            bodyContent += `
                                <tr>
                                    <td>${estado.descripcion}</td>
                                    <td class="centered">${estado.cantidadVehiculos}</td>
                                </tr>
                            `;

                            arrayEjeX.push(estado.descripcion)
                            arrayEjeY.push(estado.cantidadVehiculos)
                        });
                    }

                    bodyContent += `
                            <tr>
                                <td><strong>Total</strong></td>
                                <td class="centered">${total}</td>
                            </tr>
                        `
                    tableBody.innerHTML = bodyContent;

                    
                    myChart.setOption(option);
                    myChart.resize();
                    
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
