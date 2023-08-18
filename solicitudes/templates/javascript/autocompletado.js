$(document).ready(function() {
    //autocompletado para la direccion1
    $('#direccion1').autocomplete({
        source: function(request, response){
            $.ajax({
                url: 'solicitudes/crear',
                data: { term: request.term },
                success: function(data){
                    response(data.results);
                }
            });
        },
        minLength: 3
    });

    //autocompletado para la direccion2
    $('#direccion2').autocomplete({
        source: function(request, response){
            $.ajax({
                url: 'solicitudes/crear',
                data: { term: request.term },
                success: function(data){
                    response(data.results);
                }
            });
        },
        minLength: 3
    });
});
