function initAutocomplete() {
    var input1 = document.getElementById('direccion1');
    var latitudInput1 = document.getElementById('latitud1');
    var longitudInput1 = document.getElementById('longitud1');

    var input2 = document.getElementById('direccion2');
    var latitudInput2 = document.getElementById('latitud2');
    var longitudInput2 = document.getElementById('longitud2');

    var options = {
        types: ['address'],
        componentRestrictions: { country: 'ARG' },
    };

    var autocomplete1 = new google.maps.places.Autocomplete(input1, options);
    var autocomplete2 = new google.maps.places.Autocomplete(input2, options);

    autocomplete1.addListener('place_changed', function () {
        var place = autocomplete1.getPlace();

        if (!place.geometry || !place.geometry.location) {
            return;
        }

        var latitud = place.geometry.location.lat();
        var longitud = place.geometry.location.lng();

        latitudInput1.value = latitud;
        longitudInput1.value = longitud;

        // Guardar la dirección y sus coordenadas en un objeto o matriz.
        var direccion1 = input1.value;
        var coordenadas1 = { latitud: latitud, longitud: longitud };

        // Puedes almacenar esta información en un objeto o matriz global según tus necesidades.
        // Ejemplo con un objeto:
        var direcciones = {
            direccion1: coordenadas1,
            direccion2: coordenadas2, // Agrega más direcciones si es necesario.
        };
    });

    autocomplete2.addListener('place_changed', function () {
        var place = autocomplete2.getPlace();

        if (!place.geometry || !place.geometry.location) {
            return;
        }

        var latitud = place.geometry.location.lat();
        var longitud = place.geometry.location.lng();

        latitudInput2.value = latitud;
        longitudInput2.value = longitud;

        // Guardar la dirección y sus coordenadas en un objeto o matriz.
        var direccion2 = input2.value;
        var coordenadas2 = { latitud: latitud, longitud: longitud };

        // Puedes almacenar esta información en un objeto o matriz global según tus necesidades.
        // Ejemplo con un objeto:
        var direcciones = {
            direccion1: coordenadas1,
            direccion2: coordenadas2, // Agrega más direcciones si es necesario.
        };
    });
}



window.onload = function () {
    initAutocomplete();
};