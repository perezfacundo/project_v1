let dataTable;
let dataTableIsInitialized = false;
const myChart = echarts.init(document.getElementById("chart"));

let aVehiculos = []
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
            const listarPor = $('#listarPor').val()

            const url ='http://127.0.0.1:8000/vehiculos/reportes/';

            const datos = {
                fechaInicio: fechaInicio,
                fechaFin: fechaFin,
                listarPor: listarPor
            };

            console.log(datos)

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
                    console.log(data.vehiculos)

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
