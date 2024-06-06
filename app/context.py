from .models import Profile


def perfil_disponible(request):
    user = request.user
    profile = None
    try:
        profile = Profile.objects.get(usuario=user)
    except:
        profile = None
    return {'profile': profile}
