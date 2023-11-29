let dataTable;
let dataTableIsInitialized;

const dataTableOptions = {
    columnDefs: [{orderable: false, targets: [1]}],
    searching: false,
    dom: "Bfrtip",
    buttons: ["copy", "csv", "excel", "pdf", "print"]
};

const initDataTable = async () => {
    if (dataTableIsInitialized){
        if (dataTable) {
            dataTable.destroy();
        }
    }

    await listSolicitudes();

    try {
        dataTable = $("tableSolicitudes").DataTable(dataTableOptions);
    } catch(error) {
        alert(ex);
    }

    dataTableIsInitialized = true;
}

const listSolicitudes = async () => {
    try {
        const response = await fetch("http://127.0.0.1/solicitudes_semana/")
        const data = await response.json()
        console.log(data)
    } catch(error){
        alert(ex)
    }
}

window.addEventListener("load", async () => {
    await initDataTable();
})