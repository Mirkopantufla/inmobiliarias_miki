from .models import Profile, ContactArrendatario


def perfil_disponible(request):
    user = request.user
    profile = None
    try:
        profile = Profile.objects.get(usuario=user)
    except:
        profile = None

    return {'profile': profile}


def mensajes_disponibles(request):
    user = request.user
    mensajes = None

    try:
        mensajes = ContactArrendatario.objects.filter(id_arrendador=user).all()
    except:
        mensajes = None

    return {'mensajes': mensajes}
