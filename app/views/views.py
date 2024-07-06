from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from ..models import Inmueble, Profile, ContactForm, ContactArrendatario, TipoImagen, Imagenes
from ..forms import CustomUserCreationForm, CustomPasswordChangeForm, ContactFormModelForm, CustomAuthenticationForm, ContactArrendatarioForm, ProfileCreationForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView, LoginView, PasswordChangeDoneView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def indice(request):
    inmuebles = Inmueble.objects.all()
    casas = []
    departamentos = []
    parcelas = []

    for inmueble in inmuebles:
        if inmueble.tipo_inmueble.descripcion == 'Casa':
            casas.append(inmueble)
        elif inmueble.tipo_inmueble.descripcion == 'Departamento':
            departamentos.append(inmueble)
        elif inmueble.tipo_inmueble.descripcion == 'Parcela':
            parcelas.append(inmueble)

    context = {
        'casas': casas,
        'departamentos': departamentos,
        'parcelas': parcelas
    }

    return render(request, 'index.html', context)


def exito(request):
    return render(request, 'exito.html')


def acerca(request):
    return render(request, 'acerca.html')


def contacto(request):

    if request.method == 'POST':
        form = ContactFormModelForm(request.POST)
        # chequear que los datos son validos
        if form.is_valid():
            # Creamos los datos del formulario
            ContactForm.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/exito/')
    else:
        form = ContactFormModelForm()
    # el contexto, es el diccionario donde se envian los datos
    context = {'form': form}

    return render(request, 'contacto.html', context)


def contacto_arrendador(request, id_inmueble, id_arrendador):
    arrendatario = request.user
    inmueble = Inmueble.objects.get(id=id_inmueble)
    arrendador = User.objects.get(id=id_arrendador)

    if request.method == 'POST':
        formulario_contacto = ContactArrendatarioForm(request.POST)
        # chequear que los datos son validos
        if formulario_contacto.is_valid():
            # Creamos los datos del formulario
            oferta = formulario_contacto.cleaned_data['oferta']
            mensaje = formulario_contacto.cleaned_data['mensaje']

            datos = ContactArrendatario(
                id_arrendador=arrendador,
                id_arrendatario=arrendatario,
                id_inmueble=inmueble,
                oferta=oferta,
                mensaje=mensaje,
            )

            datos.save()
            return HttpResponseRedirect('/exito/')
    else:
        formulario_contacto = ContactArrendatarioForm()

@login_required(login_url='/login/')
def visualizar_mensaje(request, id, inmueble_id):
    inmueble = ContactArrendatario.objects.get(id=id)
    inmueble.visto = True
    inmueble.save()

    return redirect(f'/detalle-inmueble/{inmueble_id}/')


def not_found(request):
    return render(request, 'not_found.html')


def upload_image(request):
    usuario = request.user
    categoria = TipoImagen.objects.get(id=1) #Sin Asignar
    if request.method == 'POST':
        for file in request.FILES.getlist('imagenes'):

            imagen = Imagenes(
                auto_id=0,
                id_usuario=usuario,
                categoria=categoria,
                imagen=file)

            imagen.save()

    # return HttpResponseRedirect('/gestionar-inmuebles/')

def pruebas(request):
    return render(request, 'pruebas.html')

class MiVistaProtegida(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'
