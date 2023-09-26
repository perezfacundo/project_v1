const stars = document.querySelectorAll('.star');
    stars.forEach(star => {
        star.addEventListener('click', () => {
            alert('Las estrellas no se pueden cambiar en este formulario.');
        });
    });