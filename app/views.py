from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Inmueble, Profile, ContactForm, ContactArrendatario
from .forms import CustomUserCreationForm, ProfileCreationForm, CustomPasswordChangeForm, ContactFormModelForm, CustomAuthenticationForm, UserUpdateForm, InmuebleForm, ContactArrendatarioForm
from django.contrib.auth.views import PasswordChangeView, LoginView, PasswordChangeDoneView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy("password_change_success")
    template_name = 'registration/password_change.html'
    title = ("Cambio de contraseña")


class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = "registration/password_change_success.html"


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


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(
                username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            Profile.objects.create(usuario=user)
            login(request, user)
            return redirect('/profile/')
        else:
            data['form'] = user_creation_form

    return render(request, 'registration/register.html', data)


@login_required(login_url='/login/')
def registrar_inmueble(request):
    user = request.user
    if request.method == "POST":
        formulario_inmueble = InmuebleForm(request.POST)
        if formulario_inmueble.is_valid():
            nombre = formulario_inmueble.cleaned_data['nombre']
            descripcion = formulario_inmueble.cleaned_data['descripcion']
            metros_cuadrados_terreno = formulario_inmueble.cleaned_data['metros_cuadrados_terreno']
            metros_cuadrados_construidos = formulario_inmueble.cleaned_data[
                'metros_cuadrados_construidos']
            cantidad_estacionamientos = formulario_inmueble.cleaned_data[
                'cantidad_estacionamientos']
            cantidad_habitaciones = formulario_inmueble.cleaned_data['cantidad_habitaciones']
            cantidad_banios = formulario_inmueble.cleaned_data['cantidad_banios']
            precio_mensual = formulario_inmueble.cleaned_data['precio_mensual']
            direccion = formulario_inmueble.cleaned_data['direccion']
            region = formulario_inmueble.cleaned_data['region']
            comuna = formulario_inmueble.cleaned_data['comuna']
            tipo_inmueble = formulario_inmueble.cleaned_data['tipo_inmueble']

            datos = Inmueble(
                nombre=nombre,
                descripcion=descripcion,
                metros_cuadrados_terreno=metros_cuadrados_terreno,
                metros_cuadrados_construidos=metros_cuadrados_construidos,
                cantidad_estacionamientos=cantidad_estacionamientos,
                cantidad_habitaciones=cantidad_habitaciones,
                cantidad_banios=cantidad_banios,
                precio_mensual=precio_mensual,
                direccion=direccion,
                comuna=comuna,
                region=region,
                tipo_inmueble=tipo_inmueble,
                id_usuario=user,
            )
            datos.save()
            return HttpResponseRedirect('/gestionar-inmuebles/')
    else:
        formulario_inmueble = InmuebleForm()
        context = {
            'title': 'Agregar Inmueble',
            'formulario_inmueble': formulario_inmueble,
        }

        return render(request, 'registrar_inmueble.html', context)


@login_required(login_url='/login/')
def gestion_inmueble(request):
    user = request.user
    inmuebles = Inmueble.objects.filter(id_usuario=user.id)
    context = {
        'inmuebles': inmuebles
    }
    return render(request, 'gestionar_inmuebles.html', context)


@login_required(login_url='/login/')
def password_change(request):
    data = {
        'form': CustomPasswordChangeForm()
    }

    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(data=request.POST)

        if password_change_form.is_valid():
            password_change_form.save()

            return redirect('/')

    return render(request, 'registration/password_change.html', data)


def logout_view(request):
    logout(request)
    return render(request, 'registration/logout.html')


@login_required(login_url='/login/')
def profile(request):
    return render(request, 'registration/profile.html')


@login_required(login_url='/login/')
def actualizar_prefil(request):
    user = request.user
    profile = Profile.objects.filter(usuario=user).first()

    if request.method == 'POST':

        formulario_usuario = UserUpdateForm(
            request.POST, instance=user)
        if formulario_usuario.is_valid():
            User.objects.filter(id=user.id).update(
                **formulario_usuario.cleaned_data)

        formulario_perfil = ProfileCreationForm(
            request.POST, instance=profile)
        if formulario_perfil.is_valid():
            Profile.objects.filter(usuario=user).update(
                **formulario_perfil.cleaned_data)

        return HttpResponseRedirect('/profile/')
    else:
        formulario_usuario = CustomUserCreationForm(instance=user)
        formulario_perfil = ProfileCreationForm(instance=profile)

    return render(request, 'actualizar_prefil.html', {
        'formulario_usuario': formulario_usuario,
        'formulario_perfil': formulario_perfil
    })


@login_required(login_url='/login/')
def explorar_inmuebles(request):
    user = request.user
    profile = Profile.objects.get(usuario=user)
    context = {}
    if request.method == 'GET':
        if profile.tipo_usuario.descripcion == 'Arrendatario':
            inmuebles = Inmueble.objects.all()

            context = {
                'title': 'Buscar arriendos',
                'inmuebles': inmuebles
            }
        else:
            context = {
                'title': 'Como Arrendatario no puedes ver esta vista',
                'inmuebles': None
            }

    return render(request, 'explorar_inmuebles.html', context)


@login_required(login_url='/login/')
def detalle_inmueble(request, inmueble_id):
    user = request.user
    profile = Profile.objects.get(usuario=user)
    inmueble = None
    formulario_contacto = ContactArrendatarioForm()

    try:
        inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    except Http404:
        return redirect('/not-found/')

    if profile.tipo_usuario.descripcion == 'Arrendatario':
        context = {
            'title': 'Detalles Inmueble',
            'formulario_contacto': formulario_contacto,
            'inmueble': inmueble
        }
    else:
        mensajes_inmueble = ContactArrendatario.objects.filter(
            id_arrendador=user.id, id_inmueble=inmueble_id)
        context = {
            'title': 'Detalles Inmueble',
            'mensajes_inmueble': mensajes_inmueble,
            'inmueble': inmueble
        }

    return render(request, 'detalle_inmueble.html', context)


@login_required(login_url='/login/')
def modificar_inmueble(request, inmueble_id):
    user = request.user
    inmueble = None
    try:
        inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    except Http404:
        return redirect('/not-found/')

    if request.method == "POST":
        formulario_inmueble = InmuebleForm(request.POST)
        if formulario_inmueble.is_valid():
            inmueble = Inmueble.objects.filter(id=inmueble_id).update(
                **formulario_inmueble.cleaned_data)
        return HttpResponseRedirect('/gestionar-inmuebles/')

    if request.method == "GET":
        if inmueble.id_usuario.id == user.id:
            formulario_inmueble = InmuebleForm(instance=inmueble)
            context = {
                'title': 'Editar Inmueble',
                'formulario_inmueble': formulario_inmueble,
            }
        else:
            formulario_inmueble = 'Inmueble no encontrado'
            context = {
                'title': 'Usted no tiene acceso a esta propiedad',
                'formulario_inmueble': None,
            }

    return render(request, 'registrar_inmueble.html', context)


@login_required(login_url='/login/')
def eliminar_inmueble(request, inmueble_id):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    inmueble.delete()
    return redirect('/gestionar-inmuebles/')


@login_required(login_url='/login/')
def visualizar_mensaje(request, id, inmueble_id):
    inmueble = ContactArrendatario.objects.get(id=id)
    inmueble.visto = True
    inmueble.save()

    return redirect(f'/detalle-inmueble/{inmueble_id}/')


def not_found(request):
    return render(request, 'not_found.html')


class MiVistaProtegida(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'
