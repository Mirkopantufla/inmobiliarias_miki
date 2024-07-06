document.addEventListener("DOMContentLoaded", function() {
    const fileInput = document.querySelector('#id_imagen');
    const visualizador_imagen = document.querySelector('.visualizador_imagen');

    fileInput.addEventListener('change', function() {
        visualizador_imagen.innerHTML = ''; // Clear previous previews
        for (const file of fileInput.files) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.classList.add('preview_image_format')
                // img.style.width = "200px"
                // img.style.height = "200px"
                visualizador_imagen.appendChild(img);
            }
            reader.readAsDataURL(file);
        }
        if (fileInput.files) {
            visualizador_imagen.classList.remove('d-none')
            visualizador_imagen.classList.add('d-flex')
        }else{
            visualizador_imagen.classList.remove('d-flex')
            visualizador_imagen.classList.add('d-none')
        }
    });
});