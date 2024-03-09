const btnConsultar = document.getElementById("btnConsultar");

let arrayEjeX = [];
let arrayEjeY = [];

let option = {
  title: {
    text: "",
  },
  tooltip: {
    show: true,
    trigger: "axis",
    triggerOn: "mousemove|click",
  },
  toolbox: {
    feature: {
      saveAsImage: {},
    },
  },
  xAxis: [
    {
      type: "category",
      data: arrayEjeX,
      axisLabel: { rotate: 30 },
    },
  ],
  yAxis: [
    {
      type: "value",
    },
  ],
  series: [
    {
      data: arrayEjeY,
      type: "bar",
    },
  ],
};

const dataTableOptions = {
  columnDefs: [
    { className: "centered", targets: [1] },
    // { orderable: false, targets: [0, 1] },
    // { searchable: false, targets: [0, 1 ]},
  ],
  searching: false,
  ordering: false,
  destroy: true,
  dom: "Bfrtip",
  buttons: ["copy", "csv", "excel", "pdf", "print"],
};

const listReporte = async () => {
  let table = $("#tableClientes").DataTable(dataTableOptions);
  table.clear().draw();

  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const pathConsulta = "http://127.0.0.1:8000/clientes/reportes/";

  const datos = {
    fechaInicio: $("#fechaInicio").val(),
    fechaFin: $("#fechaFin").val(),
    listarPor: $("#listarPor").val(),
  };

  console.log(datos);

  const config = {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datos),
  };

  fetch(pathConsulta, config)
    .then(function (response) {
      if (response.status === 200) {
        return response.json();
      } else {
        throw new Error("Error al obtener una respuesta del servidor");
      }
    })
    .then((respuesta) => {
      let total = 0;

      console.log(respuesta);

      if (datos.listarPor === "estados") {
        option.title.text = `Reporte de clientes por estados`;

        total = 0;
        //cambiar titulos de las columnas
        $("#tableClientes thead tr th:eq(0)").text("Estado");
        $("#tableClientes thead tr th:eq(1)").text("Cantidad de clientes");

        //recorrer respuesta
        respuesta.estados.forEach((estado) => {
          total += estado.cantidadClientes;
          console.log(total);

          table.row.add([estado.descripcion, estado.cantidadClientes]).draw();

          //push datos para grafico
          arrayEjeX.push(estado.descripcion);
          arrayEjeY.push(estado.cantidadClientes);
        });

        //agregar total a la tabla
        console.log(total);
        var celdaTotal = document
          .getElementById("tableFoot")
          .getElementsByTagName("th")[1];
        celdaTotal.textContent = total;

      } else {
        option.title.text = `Reporte de clientes por cantidad de viajes`;
        total = 0;
        //cambiar titulos de las columnas
        $("#tableClientes thead tr th:eq(0)").text("Clientes");
        $("#tableClientes thead tr th:eq(1)").text("Cantidad de viajes");

        //recorrer respuesta
        respuesta.clientes.forEach((cliente) => {
          total += cliente.cantidadViajes;
          console.log(total);

          table.row.add([cliente.nombre, cliente.cantidadViajes]).draw();

          //push datos para grafico
          arrayEjeX.push(cliente.nombre);
          arrayEjeY.push(cliente.cantidadViajes);
        });

        //agregar total a la tabla
        console.log(total);
        var celdaTotal = document
          .getElementById("tableFoot")
          .getElementsByTagName("th")[1];
        celdaTotal.textContent = total;
      }

      initChart();
      reiniciarOption();
    });
};

btnConsultar.addEventListener("click", async () => {
  await listReporte();
});

const initChart = () => {
  let myChart = echarts.init(document.getElementById("chart"));
  myChart.setOption(option);
};

function reiniciarOption() {
  arrayEjeX.splice(0, arrayEjeX.length);
  arrayEjeY.splice(0, arrayEjeY.length);
}
