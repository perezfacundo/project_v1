// const btnConsultar = document.getElementById("btnConsultar")

// let arrayEjeX = []
// let arrayEjeY = []

// let option = {
//     title: {
//         text: ""
//     },
//     tooltip: {
//         show: true,
//         trigger: "axis",
//         triggerOn: "mousemove|click"
//     },
//     toolbox: {
//         feature: {
//             saveAsImage: {}
//         }
//     },
//     xAxis: [
//         {
//             type: "category",
//             data: arrayEjeX,
//             axisLabel: { rotate: 30 }
//         }
//     ],
//     yAxis: [
//         {
//             type: "value"
//         }
//     ],
//     series: [
//         {
//             data: arrayEjeY,
//             type: "bar"
//         }
//     ]
// }

// const dataTableOptions = {
//     columnDefs: [
//         { className: "centered", targets: [1] }
//     ],
//     searching: false,
//     ordering: false,
//     destroy: true,
//     dom: "Bfrtip",
//     buttons: ["copy", "csv", "excel", "pdf", "print"]
// }

// const listReporte = async () => {
//     let table = $("#tableVehiculos").DataTable(dataTableOptions)
//     table.clear().draw()

//     const csrfToken = $('input[name="csrfmiddlewaretoken"]').val()
//     const pathConsulta = "http://127.0.0.1:8000/vehiculos/reportes/"

//     const datos = {
//         fechaInicio: $("#fechaInicio").val(),
//         fechaFin: $("#FechaFin").val(),
//         listarPor: $("#listarPor").val()
//     }

//     console.log(datos)

//     const config = {
//         method: "POST",
//         headers: {
//             "X-CSRFToken": csrfToken,
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(datos)
//     }

//     fetch(pathConsulta, config)
//     .then(function (response) {
//         if (response.status === 200) {
//             return response.json()
//         } else {
//             throw new Error("Error al obtener una respuesta del servidor")
//         }
//     })
//     .then((respuesta) => {
//         let total = 0;

//         console.log(respusta)

//         if (datos.listarPor === "vehiculos") {
//             option.title.text = `Reporte por vehiculos por `

//             total = 0;

//             //cambiar titulos de las columnas
//             $("#tableVehiculos thead tr th:eq(0")
//         } else {
            
//         }
//     })
// }

//===================================================================

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
        { className: "centered", targets: [0, 1] },
        { orderable: true, targets: [1] }
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
        dataTable = $('#tableVehiculos').DataTable(dataTableOptions);
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
            const listarPor = $('#listarPor').val();
            const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

            const url = 'http://127.0.0.1:8000/vehiculos/reportes/';

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                listarPor: listarPor
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
                    let headContent = "";
                    let bodyContent = "";
                    let total = 0;

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
    myChart.setOption(option);
}

function reiniciarOption() {
    arrayEjeX.splice(0, arrayEjeX.length);
    arrayEjeY.splice(0, arrayEjeY.length);
}