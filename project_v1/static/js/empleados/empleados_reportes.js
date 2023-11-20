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
    'xAxis': [
        {
            'type': "category",
            'data': arrayEjeX
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
        { orderable: false, targets: [2] },
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

    dataTable = $('#tableEmpleados').DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listReportes = async () => {
    try {
        $('#enviarButton').click(function () {
            const fechaInicio = $('#fechaInicio').val();
            const fechaFin = $('#fechaFin').val();
            const listarPor = $('#listarPor').val();
            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

            const url = 'http://127.0.0.1:8000/empleados/reportes/'

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                listarPor: listarPor,
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
                    
                    //Proceso de la informacion
                    let total = 0;
                    let headContent = '';
                    let bodyContent = '';

                    if (listarPor === 'nombres') {

                        headContent = `
                            <tr>
                                <th class="centered">Apellidos</th>
                                <th class="centered">Nombres</th>
                                <th class="centered">Viajes</th>
                            </tr>
                        `;
                        tableHead.innerHTML = headContent;

                        data.empleados.forEach((empleado, index) => {
                            total += empleado.cantidadViajes;

                            content += `
                                <tr>
                                    <td>${empleado.last_name}</td>
                                    <td>${empleado.first_name}</td>
                                    <td class="centered">${empleado.cantidadViajes}</td>
                                </tr>
                            `;
                            arrayEjeX.push(empleado.last_name);
                            arrayEjeY.push(empleado.cantidadViajes);
                        });

                        bodyContent += `
                            <tr>
                                <td><strong>Total</strong></td>
                                <td></td>
                                <td class="centered">${total}</td>
                            </tr>
                        `;

                    } else { //listar por estados

                        headContent = `
                            <tr>
                                <th class="centered">Estado</th>
                                <th class="centered">Cantidad de empleados</th>
                            </tr>
                        `;
                        tableHead.innerHTML = headContent;

                        data.estados.forEach((empleado, index) => {
                            total += estado.cantidadEmpleados
                            content += `
                                <tr>
                                    <td>${estado.descripcion}</td>
                                    <td class="centered">${estado.cantidadEmpleados}</td>
                                </tr>
                            `;
                            arrayEjeX.push(empleado.last_name);
                            arrayEjeY.push(empleado.cantidadViajes);
                        });

                        bodyContent += `
                            <tr>
                                <td><strong>Total</strong></td>
                                <td></td>
                                <td class="centered">${total}</td>
                            </tr>
                        `;
                    }

                    tableBody.innerHTML = content;

                    initChart();

                    reiniciarOption();
                })

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
    myChart.setOption(option);
}

function reiniciarOption() {
    arrayEjeX.splice(0, arrayEjeX.length);
    arrayEjeY.splice(0, arrayEjeY.length);
}