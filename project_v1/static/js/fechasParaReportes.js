document.addEventListener("DOMContentLoaded", function () {
    //Obtener la fecha de hoy
    var fechaHoy = new Date();

    // Establecer el valor del campo de la fecha de hoy
    var fechaHoyInput = document.getElementById("fechaFin");
    fechaHoyInput.valueAsDate = fechaHoy;

    //Obtener el primer dia del mes
    var primerDiaMes = new Date(fechaHoy.getFullYear(), fechaHoy.getMonth(), 1);

    //Establecer el valor del campo del primer dia del mes
    var primerDiaMesInput = document.getElementById("fechaInicio");
    primerDiaMesInput.valueAsDate = primerDiaMes;
  });