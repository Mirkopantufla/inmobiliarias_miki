from django.contrib import admin
from .models import Profile, TipoUsuario, Inmueble, TipoInmueble, Region, Comuna, ContactForm, ContactArrendatario, Imagenes, TipoImagen

# Register your models here.
admin.site.register(Profile)
admin.site.register(TipoUsuario)
admin.site.register(Inmueble)
admin.site.register(TipoInmueble)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(ContactForm)
admin.site.register(ContactArrendatario)
admin.site.register(Imagenes)
admin.site.register(TipoImagen)
