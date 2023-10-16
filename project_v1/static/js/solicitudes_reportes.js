const form_filtros = document.getElementById("form_filtros"); 
let dataTable;
let dataTableIsInitialized = false;

const dataTableOptions = {
    columnDefs: [
        {className: 'centered', targets: [1, 2]}
    ],
    destroy: true
}

form_filtros.addEventListener("click", function(event){
    event.preventDefault();

})