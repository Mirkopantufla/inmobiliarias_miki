from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.

# Por buenas practicas, separo el dv del rut, para una supuesta verificación de rut, ya que la formula para el digito verificador arroja 10 para K y 11 para 0


class Profile(models.Model):
    usuario = models.OneToOneField(
        User, related_name='usuario', on_delete=models.CASCADE)
    segundo_nombre = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100)
    rut = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999999999)
        ]
    )  # xxx.xxx.xxx (En caso de ser empresa)
    dv = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(11)
        ]
    )  # 1-9, K=10, 0=11
    direccion = models.CharField(max_length=300)
    region = models.ForeignKey(
        'Region',
        related_name='usuario',
        on_delete=models.CASCADE
    )
    comuna = models.ForeignKey(
        'Comuna',
        related_name='usuario',
        on_delete=models.CASCADE
    )
    telefono = models.BigIntegerField()
    tipo_usuario = models.ForeignKey(
        'TipoUsuario',
        related_name='usuario',
        on_delete=models.CASCADE
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

        # Si el metodo clean es instanciado por dv, y es string
        if isinstance(self.dv, str):
            # Si la letra en minuscula es la k:
            if self.dv.lower() == 'k':
                # Se guarda un 10, representando la k
                self.dv = 10
            else:
                raise ValidationError(
                    {'dv': 'El dígito verificador (dv) debe ser un número del 0-9 o letra "k".'})

        elif isinstance(self.dv, int):
            if self.dv == 0:
                # Se guarda un 11, representando al 0
                self.dv = 11

        # Consultar de que el dv está en el rango válido después de la conversión
        if not (1 <= self.dv <= 11):
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
    metros_cuadrados_terreno = models.IntegerField(
        blank=False, null=False)  # Debe tener terreno
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
