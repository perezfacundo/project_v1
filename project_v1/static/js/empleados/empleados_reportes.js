let dataTable;
let dataTableIsInitialized = false;

let EntidadX = []
let CantidadesY = []

let chart = {
    'tooltip': {
        'show': true,
        'trigger': "axis",
        'triggerOn': "mousemove|click"
    },
    'xAxis': [
        {
            'type': "category",
            'data': EntidadX
        }
    ],
    'yAxis': [
        {
            'type': "value"
        }
    ],
    'series': [
        {
            'data': CantidadesY,
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

    dataTable = $('#table').DataTable(dataTableOptions);

    dataTableIsInitialized = true;
};

const listReportes = async () => {
    try {
        $('#enviarButton').click(function () {
            const fechaInicio = $('#fechaInicio').val();
            const fechaFin = $('#fechaFin').val();
            const listarPor = $('#listarPor').val();
            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                listarPor: listarPor,
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

                    console.log(data)
                    
                    //Proceso de la informacion
                    let total = 0;
                    let content = '';

                    if (listarPor === 'nombres') {

                        headContent = `
                            <tr>
                                <th class="centered">Apellidos</th>
                                <th class="centered">Nombres</th>
                                <th class="centered">Viajes</th>
                            </tr>
                        `
                        tablehead.innerHTML = headContent

                        data.empleados.forEach((empleado, index) => {
                            total += empleado.cantidadViajes
                            content += `
                                <tr>
                                    <td>${empleado.last_name}</td>
                                    <td>${empleado.first_name}</td>
                                    <td class="centered">${empleado.cantidadViajes}</td>
                                </tr>
                            `;
                            EntidadX.push(empleado.last_name)
                            CantidadesY.push(empleado.cantidadViajes)
                        });

                        content += `
                            <tr>
                                <td><strong>Total</strong></td>
                                <td></td>
                                <td class="centered">${total}</td>
                            </tr>
                        `

                    } else { //listar por estados

                        headContent = `
                            <tr>
                                <th class="centered">Estado</th>
                                <th class="centered">Cantidad de empleados</th>
                            </tr>
                        `
                        tablehead.innerHTML = headContent

                        data.estados.forEach((empleado, index) => {
                            total += estado.cantidadEmpleados
                            content += `
                                <tr>
                                    <td>${estado.descripcion}</td>
                                    <td class="centered">${estado.cantidadEmpleados}</td>
                                </tr>
                            `;
                            EntidadX.push(empleado.last_name)
                            CantidadesY.push(empleado.cantidadViajes)
                        });

                        content += `
                            <tr>
                                <td><strong>Total</strong></td>
                                <td></td>
                                <td class="centered">${total}</td>
                            </tr>
                        `
                    }

                    tablebody.innerHTML = content;

                    console.log(EntidadX, CantidadesY)

                    const myChart = echarts.init(document.getElementById("chart"));
                    myChart.setOption(chart);
                    myChart.resize();
                },
                error: function (error) {
                    console.log('Error: ', error)
                }
            });

            if (listarPor === 'estados') {

            }
            else {

            }

        });
    } catch (ex) {
        alert(ex);
        console.log("Error: ", ex)
    };
};

window.addEventListener("load", async () => {
    await initDataTable();
});
