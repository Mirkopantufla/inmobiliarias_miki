from django import forms
from django.forms import ModelForm
from django.core.validators import FileExtensionValidator
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .validators import validate_file_mimetype
from .models import Profile, ContactForm, Inmueble, ContactArrendatario, Imagenes


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


class ContactArrendatarioForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContactArrendatarioForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-control'
            }

    class Meta:
        model = ContactArrendatario
        fields = ['oferta', 'mensaje']
        labels = {
            'oferta': 'Oferta',
            'mensaje': 'Mensaje',
        }


class InmuebleForm(ModelForm):
    imagen = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True}
        ),
        required=False,
        validators=[FileExtensionValidator(
            ['png', 'jpeg', 'jpg']), validate_file_mimetype]
    )

    class Meta:

        model = Inmueble
        fields = (
            'nombre', 'descripcion', 'metros_cuadrados_terreno',
            'metros_cuadrados_construidos', 'cantidad_estacionamientos', 'cantidad_habitaciones',
            'cantidad_banios', 'precio_mensual', 'direccion',
            'region', 'comuna', 'tipo_inmueble'
        )
        labels = {
            'nombre': 'Titulo descriptivo',
            'descripcion': 'Descripción',
            'metros_cuadrados_terreno': 'm2 Terreno',
            'metros_cuadrados_construidos': 'm2 Construidos',
            'cantidad_estacionamientos': 'Cantidad de estacionamientos',
            'cantidad_habitaciones': 'Cantidad habitaciones',
            'cantidad_banios': 'Cantidad de baños',
            'precio_mensual': 'Precio mensual',
            'direccion': 'Direccion',
            'region': 'Region',
            'comuna': 'Comuna',
            'tipo_inmueble': 'Tipo del inmueble',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'metros_cuadrados_terreno': forms.NumberInput(attrs={'class': 'form-control'}),
            'metros_cuadrados_construidos': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_estacionamientos': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_habitaciones': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad_banios': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_mensual': forms.NumberInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'comuna': forms.Select(attrs={'class': 'form-select'}),
            'tipo_inmueble': forms.Select(attrs={'class': 'form-select'}),
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


class UserUpdateForm(ModelForm):
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


class ProfileCreationForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProfileCreationForm, self).__init__(*args, **kwargs)
        self.fields['segundo_nombre'].required = False
        self.fields['apellido_materno'].required = False

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
        widgets = {
            'segundo_nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.NumberInput(attrs={'class': 'form-control'}),
            'dv': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'comuna': forms.Select(attrs={'class': 'form-select'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-select'}),
        }


class UploadImageForm(ModelForm):

    class Meta:
        model = Imagenes
        fields = ['imagen']
        labels = {
            'imagen': "Sube imagenes"
        }
        widgets = {
            'imagen': forms.ClearableFileInput(
                attrs={
                    'multiple': True,
                    'accept': 'image/jpeg,image/png,image/jpg'
                }
            )
        }
        validators = [FileExtensionValidator(
            ['png', 'jpeg', 'jpg']), validate_file_mimetype]
