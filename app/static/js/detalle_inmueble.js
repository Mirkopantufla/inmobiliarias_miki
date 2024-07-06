// Expositor de imagenes disponibles
const contenedorPrincipal = document.getElementById("imagen-principal")
const imagenPrincipal = contenedorPrincipal.firstElementChild

const contenedorImagenes = document.getElementById("contenedor-imagenes")
const imagenes = contenedorImagenes.querySelectorAll("img")
imagenes.forEach(element => {
    element.addEventListener("mouseenter", (e) => {
        imagenPrincipal.src = element.src
    })
});

// Script que manda la informacion necesaria a el back
const contactoArrendadorModal = document.getElementById('contactoArrendadorModal');

contactoArrendadorModal.addEventListener('show.bs.modal', event => {
    // El boton que activa al modal
    const button = event.relatedTarget
    // Extraer informacion desde el atributo data-id
    const idInmuebleArrendador = button.getAttribute('data-id');
    // Llamar al formulario para poder entregarle el action junto con el id del arrendador
    const formularioContacto = document.getElementById('contactoArrendatario');
    formularioContacto.action = '/contactar-arrendador/' + idInmuebleArrendador + '/';
})