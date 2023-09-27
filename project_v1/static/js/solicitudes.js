let dataTable;
let dataTableIsInitialized = false;

function encontrarDescripcion(numero, estados) {
    const estadoEncontrado = estados.find(estado => estado.id === numero);
    if (estadoEncontrado) {
      return estadoEncontrado.descripcion;
    } else {
      return 'No se encontró una descripción para el número ' + numero;
    }
  }

const dataTableOptions={
    columnDefs:[
        {className:'centered', targets:[0,1,2,3,4,5,6]},
        {orderable: false, targets:[5,6]},
        {searchable: true, targets:[1,2,3]}
    ],
    pageLength:4,
    destroy: true
}

const initDataTable = async () => {
    if (dataTableIsInitialized) {
        dataTable.destroy();
    }
    await listSolicitudes();

    dataTable = $(`#datatable_Solicitudes`).DataTable({dataTableOptions});

    dataTableIsInitialized = true;
}

const listSolicitudes = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/solicitudes_listado/');
        const data = await response.json();
        const estados = data.estados
        const usuario = data.usuario
        console.log(data.usuario)

        let content = '';
        let estado = '';
        data.solicitudes.forEach((solicitud, index) => {
            estado = encontrarDescripcion(solicitud.id_estado_solicitud_id, estados)
            content += `
                <tr>
                    <td>${solicitud.id}</td>
                    <td>${solicitud.direccion_desde}</td>
                    <td>${solicitud.direccion_hasta}</td>
                    <td>${solicitud.fecha_trabajo}</td>
                    <td>${estado}</td>
                    <td>
                        <a class="btn btn-sm" style="background-color:#3B4C7D;" href="">
                            <i class="bi bi-star-fill" style="color:#FFFFFF"></i>
                        </a>

                        <a class="btn btn-sm" style="background-color:#357266" href="">
                        <i class="bi bi-info-circle-fill" style="color:#FFFFFF"></i>
                        </a>

                        <a class="btn btn-sm" style="background-color:#C44558" href="">
                            <i class="bi bi-trash-fill" style="color:#FFFFFF"></i>
                        </a>
                    </td>

                    <td>
                    `;
            if(solicitud.calificacion != null){
                for(var i=1; i <= solicitud.calificacion; i++){
                    content+= `
                        <i class="bi bi-star-fill" style="color:#F8DA62;"></i>
                    `
                }
            }else{content += `sin calificar`}content += `</td>`
        });
        tableBody_Solicitudes.innerHTML = content;
    } catch (ex) {
        alert(ex);
    }
};

window.addEventListener('load', async () => {
    await initDataTable();
})