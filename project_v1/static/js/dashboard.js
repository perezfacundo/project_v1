const getOptionChart1 = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/grafico_anual_solicitudes/");
      const datos = await response.json();
      return datos
    } catch (ex) {
      alert(ex);
    }
  };
  
  const getOptionChart2 = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/grafico_anual_clientes/");
      const datos = await response.json();
      console.log(datos);
      return datos
    } catch (ex) {
      alert(ex);
    }
  };

  const initCharts = async () => {
    const chart1 = echarts.init(document.getElementById("chart1"));
    const option1 = await getOptionChart1();
    chart1.setOption(option1);
    
    const chart2 = echarts.init(document.getElementById("chart2"));
    const option2 = await getOptionChart2();
    chart2.setOption(option2);
  };
  
  window.addEventListener("load", () => {
    initCharts();
  });
  