document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.querySelector('#id_imagen');
    const contenedorImagenes = document.querySelector('.contenedor_imagenes');
    const divImagenes = document.querySelector('#seccion-nuevas-imagenes')

    fileInput.addEventListener('change', function() {
        contenedorImagenes.innerHTML = ''; // Clear previous previews

        for (const file of fileInput.files) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('preview_image_format')
                contenedorImagenes.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
        if (fileInput.files) {
            divImagenes.classList.remove('d-none')
            divImagenes.classList.add('d-flex')
        }else{
            divImagenes.classList.remove('d-flex')
            divImagenes.classList.add('d-none')
        }
    });
});