from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.db.models import Q
from ..models import Inmueble, Imagenes, Profile, ContactArrendatario, TipoImagen
from ..forms import InmuebleForm, ContactArrendatarioForm
from django.http import Http404
from django.db.utils import OperationalError, ProgrammingError

# ---------------------------------------- EXPLORAR TODOS LOS INMUEBLES ----------------------------------------
@login_required(login_url='/login/')
def explorar_inmuebles(request):
    user = request.user
    profile = Profile.objects.get(usuario=user)
    context = {}
    if request.method == 'GET':
        #Condiciono a que si el usuario es arrendatario, le brindo los inmuebles
        if profile.tipo_usuario.descripcion == 'Arrendatario':
            try:
                inmuebles = Inmueble.objects.filter(~Q(id_usuario=user))
            except (OperationalError, ProgrammingError) as e:
                inmuebles = []
                print(e)
            

            context = {
                'title': 'Buscar arriendos',
                'inmuebles': inmuebles
            }
        #De lo contrario, no puede ver esta vista
        else:
            context = {
                'title': 'Como Arrendatario no puedes ver esta vista',
                'inmuebles': None
            }

    return render(request, 'explorar_inmuebles.html', context)

# ---------------------------------------- GESTIONAR TUS INMUEBLES ----------------------------------------

@login_required(login_url='/login/')
def gestion_inmueble(request):
    user = request.user
    inmuebles = Inmueble.objects.filter(id_usuario=user.id)
    context = {
        'inmuebles': inmuebles
    }
    return render(request, 'gestionar_inmuebles.html', context)


# ---------------------------------------- DETALLE DE UN INMUEBLE ----------------------------------------
def detalle_inmueble(request, inmueble_id):
    user = request.user
    inmueble = None
    formulario_contacto = ContactArrendatarioForm()

    try:
        profile = Profile.objects.get(usuario=user)
    except :
        profile = None

    try:
        inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    except Http404:
        return redirect('/not-found/')

    #Busco las imagenes asociadas a este inmueble por su id
    imagenes_inmueble = Imagenes.objects.filter(id_inmueble = inmueble_id)
    if not profile == None:
        if profile.tipo_usuario.descripcion == 'Arrendatario':
            context = {
                'title': 'Detalles Inmueble',
                'formulario_contacto': formulario_contacto,
                'inmueble': inmueble,
                'imagenes_inmueble': imagenes_inmueble
            }
        else:
            #Si el usuario es arrendador, y dueño de la propiedad, le brindo los mensajes asociados
            mensajes_inmueble = ContactArrendatario.objects.filter(id_arrendador=user.id, id_inmueble=inmueble_id)
        
            context = {
                'title': 'Detalles Inmueble',
                'mensajes_inmueble': mensajes_inmueble,
                'inmueble': inmueble,
                'imagenes_inmueble': imagenes_inmueble
            }
    else:
        context = {
            'title': 'Detalles Inmueble',
            'inmueble': inmueble,
            'imagenes_inmueble': imagenes_inmueble
        }

    return render(request, 'detalle_inmueble.html', context)

@login_required(login_url='/login/')
def registrar_inmueble(request):
    user = request.user
    categoria_imagen = TipoImagen.objects.get(id=2) #2 = Inmueble
    if request.method == "POST":
        formulario_inmueble = InmuebleForm(request.POST, request.FILES)
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


            nuevo_inmueble = Inmueble(
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
            
            nuevo_inmueble.save()

            for img in request.FILES.getlist('imagen'):

                nueva_imagen = Imagenes(
                    auto_id = 0,
                    id_usuario = user,
                    categoria = categoria_imagen,
                    id_inmueble = nuevo_inmueble,
                    imagen = img
                )
                
                nueva_imagen.save()
            
            return HttpResponseRedirect(f'/detalle-inmueble/{nuevo_inmueble.id}/')
    else:
        formulario_inmueble = InmuebleForm()
        context = {
            'title': 'Agregar Inmueble',
            'formulario_inmueble': formulario_inmueble,
        }

        return render(request, 'registrar_inmueble.html', context)

@login_required(login_url='/login/')
def modificar_inmueble(request, inmueble_id):
    categoria_imagen = TipoImagen.objects.get(id=2) #2 = Inmueble
    user = request.user
    inmueble = None
    try:
        inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    except Http404:
        return redirect('/not-found/')

    if request.method == "POST":
        formulario_inmueble = InmuebleForm(request.POST)
        if formulario_inmueble.is_valid():
            
            Inmueble.objects.filter(id = inmueble_id).update(
                nombre = formulario_inmueble.cleaned_data['nombre'],
                descripcion = formulario_inmueble.cleaned_data['descripcion'],
                metros_cuadrados_terreno = formulario_inmueble.cleaned_data['metros_cuadrados_terreno'],
                metros_cuadrados_construidos = formulario_inmueble.cleaned_data[
                    'metros_cuadrados_construidos'],
                cantidad_estacionamientos = formulario_inmueble.cleaned_data[
                    'cantidad_estacionamientos'],
                cantidad_habitaciones = formulario_inmueble.cleaned_data['cantidad_habitaciones'],
                cantidad_banios = formulario_inmueble.cleaned_data['cantidad_banios'],
                precio_mensual = formulario_inmueble.cleaned_data['precio_mensual'],
                direccion = formulario_inmueble.cleaned_data['direccion'],
                region = formulario_inmueble.cleaned_data['region'],
                comuna = formulario_inmueble.cleaned_data['comuna'],
                tipo_inmueble = formulario_inmueble.cleaned_data['tipo_inmueble']
            )

            for img in request.FILES.getlist('imagen'):

                nueva_imagen = Imagenes(
                    auto_id = 0,
                    id_usuario = user,
                    categoria = categoria_imagen,
                    id_inmueble = inmueble,
                    imagen = img
                )
                
                nueva_imagen.save()

            # Inmueble.objects.filter(id = inmueble_id).update(
            #     **formulario_inmueble.cleaned_data)
            # imagenes = Imagenes.objects.filter(id_inmueble = inmueble_id).all()
            # # for imagen in imagenes:
            # #     print(imagen)

        return HttpResponseRedirect('/gestionar-inmuebles/')

    if request.method == "GET":
        imagenes = Imagenes.objects.filter(id_inmueble = inmueble_id).all()
        if inmueble.id_usuario.id == user.id:
            formulario_inmueble = InmuebleForm(instance=inmueble)
            context = {
                'title': 'Editar Inmueble',
                'formulario_inmueble': formulario_inmueble,
                'imagenes': imagenes,
            }
        else:
            formulario_inmueble = 'Inmueble no encontrado'
            context = {
                'title': 'Usted no tiene acceso a esta propiedad',
                'formulario_inmueble': None,
                'imagenes': None,
            }

    return render(request, 'registrar_inmueble.html', context)

@login_required(login_url='/login/')
def eliminar_inmueble(request, inmueble_id):
    inmueble = Inmueble.objects.get(id=inmueble_id)
    inmueble.delete()
    return redirect('/gestionar-inmuebles/')