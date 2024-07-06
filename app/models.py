from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from cloudinary.models import CloudinaryField
from django.db import models
import locale
import uuid

# Create your models here.

# Por buenas practicas, separo el dv del rut, para una supuesta verificación de rut, ya que la formula para el digito verificador arroja 10 para K y 11 para 0
ext_validation = FileExtensionValidator(['png', 'jpeg', 'jpg'])

class Profile(models.Model):
    usuario = models.OneToOneField(
        User, related_name='usuario', on_delete=models.CASCADE)
    segundo_nombre = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    # xxx.xxx.xxx (En caso de ser empresa)
    rut = models.IntegerField(null=True, blank=True)
    dv = models.SmallIntegerField(null=True, blank=True)  # 1-9, K=10, 0=11
    direccion = models.CharField(max_length=300, null=True, blank=True)
    region = models.ForeignKey(
        'Region',
        related_name='usuario',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    comuna = models.ForeignKey(
        'Comuna',
        related_name='usuario',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    telefono = models.BigIntegerField(null=True, blank=True)
    tipo_usuario = models.ForeignKey(
        'TipoUsuario',
        related_name='usuario',
        on_delete=models.CASCADE,
        default=2
    )

    # Funcion que formatea el digito verificador en caso de ser 10 u 11
    def mostrar_dv(self):
        if self.dv == 10:
            return 'k'
        elif self.dv == 11:
            return 0
        else:
            return self.dv

    def __str__(self):
        return f'{self.usuario} {self.rut}-{self.dv}'

    # Sobreescribo el metodo clean por defecto, para validar el digito verificador
    def clean(self):
        super().clean()

        print(self.dv)
        if self.rut == None:
            self.dv = None

        # Si el metodo clean es instanciado por dv, y es string
        if isinstance(self.dv, str):
            caracter = self.dv
            number = 12
            try:
                int(caracter)
                number = int(caracter)
            except ValueError:
                print('pase')
                pass

            # Si la letra en minuscula es la k:
            if caracter.lower() == 'k':
                # Se guarda un 10, representando la k
                self.dv = 10
            elif 1 <= number <= 11:
                self.dv = number
            else:
                raise ValidationError(
                    {'dv': 'El dígito verificador (dv) debe ser un número del 0-9 o letra "k".'})

        elif isinstance(self.dv, int):
            if self.dv == 0:
                # Se guarda un 11, representando al 0
                self.dv = 11

        # Consultar de que el dv está en el rango válido después de la conversión
        if not (self.dv == None or 1 <= self.dv <= 11):
            raise ValidationError(
                {'dv': 'El dígito verificador (dv) debe estar entre 1 y 11'})

    def __str__(self) -> str:
        return f'{self.usuario} {self.rut}-{self.dv}'


class TipoUsuario(models.Model):
    CHOICES = [
        ('Arrendador', 'Arrendador'),
        ('Arrendatario', 'Arrendatario')
    ]
    descripcion = models.CharField(choices=CHOICES)

    def __str__(self):
        return self.descripcion


class Inmueble(models.Model):
    # Se debe asignar un nombre
    nombre = models.CharField(max_length=200, blank=False, null=False)
    # Debe tener alguna descripcion
    descripcion = models.TextField(blank=False, null=False)
    metros_cuadrados_terreno = models.IntegerField(blank=False, null=False)  # Debe tener terreno
    metros_cuadrados_construidos = models.IntegerField(default=0)
    cantidad_estacionamientos = models.SmallIntegerField(default=0)
    cantidad_habitaciones = models.SmallIntegerField(default=0)
    cantidad_banios = models.SmallIntegerField(default=0)
    precio_mensual = models.FloatField(default=0)
    # Debe estar ubicado en algun lugar
    direccion = models.CharField(max_length=100, blank=False, null=False)
    region = models.ForeignKey(
        'Region',
        related_name='inmueble',
        on_delete=models.CASCADE
    )
    comuna = models.ForeignKey(
        'Comuna',
        related_name='inmueble',
        on_delete=models.CASCADE
    )
    tipo_inmueble = models.ForeignKey(
        'TipoInmueble',
        related_name='inmueble',
        on_delete=models.CASCADE
    )
    id_usuario = models.ForeignKey(
        User,
        related_name='inmueble',
        on_delete=models.CASCADE
    )

    # def format_price(self):
    #     formated = "{:,}".format(self.precio_mensual).replace(",", ".")
    #     return formated
    
    
    def format_price(self):
        precio = self.precio_mensual.__round__()
        formated = "{:,}".format(precio).replace(",", ".")
        return formated
        
    # def format_price(self):
    #     locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    #     return locale.currency(self.precio_mensual, grouping=True)

    def __str__(self) -> str:
        return f'{self.nombre} / {self.descripcion}'


class TipoInmueble(models.Model):
    CHOICES = [
        ('Parcela', 'Parcela'),
        ('Casa', 'Casa'),
        ('Departamento', 'Departamento')
    ]
    descripcion = models.TextField(choices=CHOICES)

    def __str__(self):
        return self.descripcion


class Region(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    numero_romano = models.CharField(max_length=10, blank=False, null=False)
    numero_region = models.SmallIntegerField(blank=False, null=False)
    abreviacion = models.CharField(max_length=4)

    def __str__(self) -> str:
        return f'{self.nombre}'


class Comuna(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    region_id = models.ForeignKey(
        'Region',
        related_name='comuna',
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f'{self.nombre}'


class ContactForm(models.Model):
    contact_form_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    customer_email = models.EmailField()
    customer_name = models.CharField(max_length=64)
    message = models.TextField()

    def __str__(self):
        return f"{self.customer_email} - Mensaje: {self.message}"


class ContactArrendatario(models.Model):
    id_arrendador = models.ForeignKey(User, related_name='contactoArrendador', on_delete=models.CASCADE)
    id_arrendatario = models.ForeignKey(User, related_name='contactoArrendatario', on_delete=models.CASCADE)
    id_inmueble = models.ForeignKey('Inmueble', related_name='contactoArrendatario', on_delete=models.CASCADE)
    visto = models.BooleanField(default=False)
    oferta = models.IntegerField()
    mensaje = models.TextField(max_length=2000)
    creacion_registro = models.DateField(auto_now_add=True)

    def format_price(self):
        precio = self.oferta.__round__()
        formated = "{:,}".format(precio).replace(",", ".")
        return formated

    def format_price(self):
        formated = str("{:,}".format(self.oferta).replace(",", "."))
        return ''.join(formated.split(-2))

    # def format_price(self):
        
    #     locale.setlocale(locale.LC_ALL, 'es_CL.UTF-8')
    #     return locale.currency(self.oferta, grouping=True)

    def __str__(self):
        return f"{self.id_arrendatario} - Mensaje: {self.mensaje}"


class Imagenes(models.Model):
    auto_id = models.IntegerField()
    id_usuario = models.ForeignKey(User, related_name='imagenes', on_delete=models.CASCADE)
    categoria = models.ForeignKey('TipoImagen', related_name='tipoImagen', on_delete=models.CASCADE)
    id_inmueble = models.ForeignKey(
        'Inmueble',
        related_name='inmuebles',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    imagen = CloudinaryField(
        'imagen',
        folder="inmueblesMiki",
        validators=[ext_validation],
        resource_type="image",
        use_filename=True,
        unique_filename=False)

    #LLave unica compuesta por categoria y id autoincrementable
    class Meta:
        unique_together = (('categoria', 'id'))


    #Calcula el valor máximo de numero para la categoria dada y lo incrementa en 1.
    #Para dar consistencia en id por categoria
    def save(self, *args, **kwargs):
        if not self.pk:
            max_id = Imagenes.objects.filter(categoria=self.categoria).aggregate(models.Max('auto_id'))['auto_id__max']
            self.auto_id = (max_id or 0) + 1
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return  f"{self.categoria.descripcion} - {self.auto_id}"

class TipoImagen(models.Model):
    descripcion = models.TextField(max_length=100)

    def __str__(self) -> str:
        return self.descripcion
