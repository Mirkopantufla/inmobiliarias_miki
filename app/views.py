from django.urls import reverse_lazy
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Inmueble, Profile, ContactForm
from .forms import CustomUserCreationForm, ProfileCreationForm, CustomPasswordChangeForm, ContactFormModelForm, CustomAuthenticationForm, UserUpdateForm
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

    context = {
        'inmuebles': inmuebles
    }
    return render(request, 'index.html', context)


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
def update_profile(request):
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

    return render(request, 'update_profile.html', {
        'formulario_usuario': formulario_usuario,
        'formulario_perfil': formulario_perfil
    })


class MiVistaProtegida(LoginRequiredMixin, TemplateView):
    template_name = 'login.html'
