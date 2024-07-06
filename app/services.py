from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Profile, TipoUsuario, Inmueble, TipoInmueble, Region, Comuna, Imagenes

# User data
# username, first_name, last_name, email, user_permissions, is_staff, is_active, is_superuser, last_login


def listar_usuarios_perfiles():
    usuarios_perfiles = Profile.objects.select_related('usuario').all()

    for user in usuarios_perfiles:
        date_time = user.usuario.last_login.strftime(
            "%d-%m-%Y %H:%M:%S")

        print(f"""
Usuario: {user.usuario.username}
Ultimo login: {date_time}
Nombres: {user.usuario.first_name} {user.segundo_nombre}
Apellidos: {user.usuario.last_name} {user.segundo_apellido}
Rut: {user.rut}-{user.dv}
Telefono: {user.telefono}
Email: {user.usuario.email}
Tipo usuario: {user.tipo_usuario}
Region: {user.region}
Comuna: {user.comuna}
Direccion: {user.direccion}
""")

    return usuarios_perfiles


def buscar_usuario(id):
    usuario_encontrado = Profile.objects.select_related(
        'usuario').get(id=id)

    if not usuario_encontrado:
        return 'Usuario inexistente'

    date_time = usuario_encontrado.usuario.last_login.strftime(
        "%d-%m-%Y %H:%M:%S")

    print(f"""
ID: {usuario_encontrado.id}
Ultimo login: {date_time}
Nombres: {usuario_encontrado.usuario.first_name} {usuario_encontrado.segundo_nombre}
Apellidos: {usuario_encontrado.usuario.last_name} {usuario_encontrado.segundo_apellido}
Rut: {usuario_encontrado.rut}-{usuario_encontrado.dv}
Telefono: {usuario_encontrado.telefono}
Email: {usuario_encontrado.usuario.email}
Tipo usuario: {usuario_encontrado.tipo_usuario}
Region: {usuario_encontrado.region}
Comuna: {usuario_encontrado.comuna}
Direccion: {usuario_encontrado.direccion}
""")
    return usuario_encontrado


def listar_inmuebles():
    inmuebles = Inmueble.objects.select_related(
        'region', 'comuna', 'tipo_inmueble').all()

    for inmueble in inmuebles:
        print(f"""
Nombre: {inmueble.nombre}
Descripcion: {inmueble.descripcion}
M2 Terreno: {inmueble.metros_cuadrados_terreno}
M2 Construidos: {inmueble.metros_cuadrados_construidos}
Cant. Estacionamientos: {inmueble.cantidad_estacionamientos}
Cant. Habitaciones: {inmueble.cantidad_habitaciones}
Cant. baños: {inmueble.cantidad_banios}
Direccion: {inmueble.direccion}
Precio Mensual: {inmueble.precio_mensual}
Region: {inmueble.region.nombre}
Comuna: {inmueble.comuna.nombre}
Tipo Inmueble: {inmueble.tipo_inmueble.descripcion}
"""
              )


def crear_inmueble(nombre, descripcion, metros_cuadrados_terreno, metros_cuadrados_construidos, cantidad_estacionamientos, cantidad_habitaciones, cantidad_banios, direccion, precio_mensual, region_id, comuna_id, tipo_inmueble_id):

    region = Region.objects.get(id=region_id)
    comuna = Comuna.objects.get(id=comuna_id)
    tipo_inmueble = TipoInmueble.objects.get(id=tipo_inmueble_id)

    nuevo_inmueble = Inmueble(
        nombre=nombre,
        descripcion=descripcion,
        metros_cuadrados_terreno=metros_cuadrados_terreno,
        metros_cuadrados_construidos=metros_cuadrados_construidos,
        cantidad_estacionamientos=cantidad_estacionamientos,
        cantidad_habitaciones=cantidad_habitaciones,
        cantidad_banios=cantidad_banios,
        direccion=direccion,
        precio_mensual=precio_mensual,
        region=region,
        comuna=comuna,
        tipo_inmueble=tipo_inmueble
    )

    # Validacion previa a guardar el chofer
    try:
        nuevo_inmueble.full_clean()  # Esto ejecutará todas las validaciones
    except ValidationError as e:
        # Manejo los errores de validación, saldra de la funcion mostrando un mensaje de error
        return {'error': str(e)}

    nuevo_inmueble.save()
    print('Inmueble creado correctamente')
    return nuevo_inmueble


# Ocupo kwargs ya que no siempre se modificaran todos los campos
# nombre, descripcion, metros_cuadrados_terreno, metros_cuadrados_construidos, cantidad_estacionamientos,
# cantidad_habitaciones, cantidad_banios, direccion, precio_mensual, region_id, comuna_id, tipo_inmueble_id
def modificar_inmueble(id_inmueble, **kwargs):
    inmueble = Inmueble.objects.get(id=id_inmueble)
    lista_modificados = []

    # Aplicar funciones específicas a los datos de kwargs
    if 'nombre' in kwargs:
        kwargs['nombre'] = kwargs['nombre'].strip().title()

    if 'descripcion' in kwargs:
        kwargs['descripcion'] = kwargs['descripcion'].strip()

    if 'metros_cuadrados_terreno' in kwargs:
        kwargs['metros_cuadrados_terreno'] = int(
            kwargs['metros_cuadrados_terreno'])

    if 'metros_cuadrados_construidos' in kwargs:
        kwargs['metros_cuadrados_construidos'] = int(
            kwargs['metros_cuadrados_construidos'])

    if 'cantidad_estacionamientos' in kwargs:
        kwargs['cantidad_estacionamientos'] = int(
            kwargs['cantidad_estacionamientos'])

    if 'cantidad_habitaciones' in kwargs:
        kwargs['cantidad_habitaciones'] = int(kwargs['cantidad_habitaciones'])

    if 'cantidad_banios' in kwargs:
        kwargs['cantidad_banios'] = int(kwargs['cantidad_banios'])

    if 'direccion' in kwargs:
        kwargs['direccion'] = kwargs['direccion'].strip()

    if 'precio_mensual' in kwargs:
        kwargs['precio_mensual'] = float(kwargs['precio_mensual'])

    if 'region_id' in kwargs:
        kwargs['region_id'] = int(kwargs['region_id'])

    if 'comuna_id' in kwargs:
        kwargs['comuna_id'] = int(kwargs['comuna_id'])

    if 'tipo_inmueble_id' in kwargs:
        kwargs['tipo_inmueble'] = int(kwargs['tipo_inmueble'])

    # Actualizar los campos del objeto Inmueble
    for key, value in kwargs.items():
        lista_modificados.append(key)
        setattr(inmueble, key, value)

    # Validacion previa a guardar el chofer
    try:
        inmueble.full_clean()  # Esto ejecutará todas las validaciones
    except ValidationError as e:
        # Manejo los errores de validación, saldra de la funcion mostrando un mensaje de error
        return {'error': str(e)}

    inmueble.save()
    for modificados in lista_modificados:
        print(f'{modificados} modificado.')
    return inmueble


def eliminar_inmueble(id_inmueble):
    inmueble = Inmueble.objects.get(id=id_inmueble)

    if inmueble:
        inmueble.delete()
        print('Inmueble eliminado')
    else:
        print('Inmueble no encontrado')

# ----------------------------------------------------------------------------------------------------------------------------
# Creador de txt con querys


def inmuebles_comuna_especifica(comuna):
    # Ejemplo realizado por el profe (comuna en especifico)

    select = f"""
    SELECT inmueble.id, inmueble.nombre, inmueble.descripcion, inmueble.comuna_id, comuna.nombre FROM app_inmueble AS inmueble
    INNER JOIN app_comuna AS comuna
    ON inmueble.comuna_id = comuna.id
    WHERE comuna.nombre like '{comuna}'
    """

    query = Inmueble.objects.raw(select)

    with open('generated/inmuebles_comuna_especifica.txt', 'w', encoding='utf-8') as archivo:
        # crear el archivo con la salida
        archivo.write(
            f'---------------- {comuna} ----------------' + '\n')
        archivo.write('ID   /   Nombre   /   Descripcion' + '\n')
        for inmueble in query:
            archivo.write(
                f"{inmueble.id} - {inmueble.nombre} - {inmueble.descripcion}" + '\n')
        archivo.close()


def inmuebles_por_comuna():

    # Consultar listado de inmuebles para arriendo separado por comunas, solo usando los
    # campos "nombre" y "descripción" en un script python que se conecta a la DB usando
    # DJango y SQL guardando los resultados en un archivo de texto

    select = f"""
    SELECT inmueble.id, inmueble.nombre, inmueble.descripcion, comuna.nombre FROM app_inmueble AS inmueble
    INNER JOIN app_comuna AS comuna
    ON inmueble.comuna_id = comuna.id
    ORDER BY comuna.nombre
    """

    query = Inmueble.objects.raw(select)

    # crear el archivo con la salida
    with open('generated/inmuebles_comuna.txt', 'w', encoding='utf-8') as archivo:
        nombreComuna = ''

        for inmueble in query:
            # Si el nombre que estoy recorriendo es distinto al anterior, es otra comuna
            if inmueble.comuna.nombre != nombreComuna:
                # Imprimo el nombre de la comuna para separarlos
                archivo.write(
                    '\n' + f'-------------------------------- {inmueble.comuna.nombre} --------------------------------' + '\n')
                nombreComuna = inmueble.comuna.nombre
            # Por cada vuelta debe imprimir los datos
            archivo.write(
                f"{inmueble.nombre} - {inmueble.descripcion}" + '\n')

        archivo.close()


def inmuebles_por_region():

    # Consultar listado de inmuebles para arriendo separado por regiones en un script
    # python que se conecta a la DB usando DJango y SQL guardando los resultados en un
    # archivo de texto.

    select = f"""
    SELECT * FROM app_inmueble AS inmueble
    INNER JOIN app_region AS region
    ON inmueble.region_id = region.id
    """

    query = Inmueble.objects.raw(select)

    # crear el archivo con la salida
    with open('generated/inmuebles_region.txt', 'w', encoding='utf-8') as archivo:
        nombreRegion = ''

        for inmueble in query:
            # Si el nombre que estoy recorriendo es distinto al anterior, es otra comuna
            if inmueble.region.nombre != nombreRegion:
                # Imprimo el nombre de la region para separarlos
                archivo.write(
                    '\n' + f'-------------------------------- {inmueble.region.numero_romano} {inmueble.region.nombre} --------------------------------' + '\n')
                nombreRegion = inmueble.region.nombre
            # Por cada vuelta debe imprimir los datos
            archivo.write(
                f"""---- ID: {inmueble.id} ----
Nombre: {inmueble.nombre}
Descripcion: {inmueble.descripcion}
M2 Terreno: {inmueble.metros_cuadrados_terreno}
M2 Construidos: {inmueble.metros_cuadrados_construidos}
Cant. Estacionamientos: {inmueble.cantidad_estacionamientos}
Cant. Habitaciones: {inmueble.cantidad_habitaciones}
Cant. Baños: {inmueble.cantidad_banios}
Direccion: {inmueble.direccion}
Precio Mensual: {inmueble.precio_mensual}
Region: {inmueble.region.nombre}
Comuna: {inmueble.comuna.nombre}
Tipo Inmueble: {inmueble.tipo_inmueble.descripcion}

""")

        archivo.close()


def obtener_imagenes():
    imagenes = Imagenes.objects.all()
    for imagen in imagenes:
        print(f"""ID: {imagen.auto_id}
Usuario: {imagen.id_usuario}
Categoria: {imagen.categoria}
Inmueble: {imagen.id_inmueble.nombre}
URL: {imagen.imagen.url}
Tipo IMG: {imagen.imagen.type}
""")
    return True
