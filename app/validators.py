import magic
from django.core.exceptions import ValidationError

#Funcion para darle mas seguridad en la subida a archivos
def validate_file_mimetype(file):
    accept = ['image/jpg', 'image/png', 'image/jpeg'] #Acepta estos tipos de imagen
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    if file_mime_type not in accept:
        raise ValidationError("Tipo de archivo no soportado")