let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    // columnDefs: [
    //     { className: 'centered', targets: [0, 1, 2, 3, 4, 5, 6] },
    //     { orderable: false, targets: [4, 5, 6] },
    //     { searchable: false, targets: [4, 5, 6] }
    // ],
    pageLength: 5,
    destroy: true
}

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listSolicitudes();

    try {
        dataTable = $(`#datatable_Solicitudes`).DataTable({ ...dataTableOptions });
        $('#dataTable_Solicitudes').find('tbody td').css('font-size', '12px');
    } catch (ex) {
        alert(ex)
    }

    dataTableIsInitialized = true;
}

const listSolicitudes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/solicitudes_reportes/');
        const data = await response.json();
        const estados = data.estados

        let content = '';


        data.solicitudes.forEach((solicitud, index) => {

        });

        tableBody_Solicitudes.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
})