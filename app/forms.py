from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, ContactForm


class ContactFormModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactFormModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = ContactForm
        fields = ['customer_email',
                  'customer_name', 'message']
        labels = {
            'customer_email': 'Correo',
            'customer_name': 'Nombre',
            'message': 'Mensaje',
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=("Contraseña Antigua"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label=("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label=("Repita nueva contraseña"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
        labels = {
            'username': 'Usuario',
            'first_name': 'Primer Nombre',
            'last_name': 'Apellido Paterno',
            'email': 'Correo',
            'password1': 'Contrasenia',
            'password2': 'Repita Contraseña'
        }


class UserUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = User
        fields = ['first_name', 'last_name',
                  'email']
        labels = {
            'first_name': 'Primer Nombre',
            'last_name': 'Apellido Paterno',
            'email': 'Correo'
        }


class ProfileCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['segundo_nombre'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['apellido_materno'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['rut'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['dv'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['direccion'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['telefono'].widget.attrs = {
            'class': 'form-control',
        }
        self.fields['region'].widget.attrs = {
            'class': 'form-select',
            'aria-label': 'Regiones'
        }
        self.fields['comuna'].widget.attrs = {
            'class': 'form-select',
            'aria-label': 'Comunas'
        }
        self.fields['tipo_usuario'].widget.attrs = {
            'class': 'form-select',
            'aria-label': 'Tipo_usuario'
        }

    class Meta:
        model = Profile
        fields = ['segundo_nombre', 'apellido_materno', 'rut', 'dv',
                  'direccion', 'telefono', 'region', 'comuna', 'tipo_usuario']
        labels = {
            'segundo_nombre': 'Segundo Nombre',
            'apellido_materno': 'Apellido Materno',
            'rut': 'Rut',
            'dv': 'Digito Verificador',
            'direccion': 'Dirección',
            'telefono': 'Telefono Celular',
            'region': 'Escoga una Región',
            'comuna': 'Escoga una Comuna',
            'tipo_usuario': 'Tipo de Usuario'
        }
