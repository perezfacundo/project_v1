getOptionChart1 = async () => {
    try{
        const response = await fetch("http://127.0.0.1:8000/grafico_solicitudes/");

        const datos = await response.json()

        return await datos
    
    }catch(ex){
        alert(ex);
    }
}

getOptionChart2 = async () => {

}

const initCharts = async () => {
    const chart1 = echarts.init(document.getElementById("chart1"));
    const chart2 = echarts.init(document.getElementById("chart2"));

    console.log(getOptionChart1())
    chart1.setOption(getOptionChart1()); 
    chart2.setOption(getOptionChart2());

    chart1.resize()
    chart2.resize()
}

window.addEventListener("load", async () => {
    await initCharts();
});