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
  columnDefs: [{ className: "centered", targets: [1] }],
  searching: false,
  ordering: false,
  destroy: true,
  dom: "Bfrtip",
  buttons: ["copy", "csv", "excel", "pdf", "print"],
};

const listReporte = async () => {
  let table = $("#tableEmpleados").DataTable(dataTableOptions);
  table.clear().draw();

  const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  const pathConsulta = "http://127.0.0.1:8000/empleados/reportes/";

  const datos = {
    fechaInicio: $("#fechaInicio").val(),
    fechaFin: $("#fechaFin").val(),
    listarPor: $("#listarPor").val(),
  };

  console.log(datos)

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
    .then((data) => {
      let total = 0;
      console.log(data);

      if (datos.listarPor === "nombres") {
        //listar por nombres
        option.title.text = `Reporte de empleados por viajes`;

        total = 0;

        //cambiar titulos de las columnas
        $("#tableEmpleados thead tr th:eq(0)").text("Nombres");
        $("#tableEmpleados thead tr th:eq(1)").text("Viajes");

        console.log(table)

        //recorrer data
        data.empleados.forEach((empleado) => {
          console.log(total)
          total += empleado.cantidadSolicitudes;
          table.row.add([empleado.nombre, empleado.cantidadSolicitudes]).draw();

          arrayEjeX.push(empleado.nombre);
          arrayEjeY.push(empleado.cantidadSolicitudes);
        });

        //agregar total a la salida
        console.log(total);
        var celdaTotal = document
          .getElementById("tableFoot")
          .getElementsByTagName("th")[1];
        celdaTotal.textContent = total;
      } else {
        //listar por estados
        option.title.text = `Reporte de empleados por estados`;

        total = 0;

        //cambiar titulos de las columnas
        $("#tableEmpleados thead tr th:eq(0)").text("Estado");
        $("#tableEmpleados thead tr th:eq(1)").text("Cantidad de empleados");

        data.estados.forEach((estado) => {
          total += estado.cantidadEmpleados;
          table.row.add([estado.descripcion, estado.cantidadEmpleados]).draw();

          arrayEjeX.push(estado.descripcion);
          arrayEjeY.push(estado.cantidadEmpleados);
        });

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
