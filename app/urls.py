from django.urls import path, include
from .views import indice, register, exito, logout_view, profile, actualizar_prefil, acerca, pruebas, upload_image, gestion_inmueble, explorar_inmuebles, detalle_inmueble, visualizar_mensaje, contacto, contacto_arrendador, not_found, registrar_inmueble, modificar_inmueble, upload_image, eliminar_inmueble, CustomPasswordChangeView, CustomLoginView, CustomPasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', indice, name='indice'),
    path('pruebas/', pruebas, name='pruebas'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('acerca/', acerca, name='acerca'),
    path('exito/', exito, name='exito'),
    path('contacto/', contacto, name='contacto'),
    path('not-found/', not_found, name='not_found'),
    path('upload_image/', upload_image, name='upload_image'),
    path('gestionar-inmuebles/', gestion_inmueble, name='gestionar_inmuebles'),
    path('actualizar-perfil/', actualizar_prefil, name='actualizar_prefil'),
    path('explorar-inmuebles/', explorar_inmuebles, name='explorar_inmuebles'),
    path('registrar-inmueble/', registrar_inmueble, name='registrar_inmueble'),
    path('detalle-inmueble/<int:inmueble_id>/',
         detalle_inmueble, name='detalle_inmueble'),
    path('contactar-arrendador/<int:id_inmueble>/<int:id_arrendador>/',
         contacto_arrendador, name='contacto_arrendador'),
    path('actualizar-inmueble/<int:inmueble_id>/',
         modificar_inmueble, name='update_inmueble'),
    path('eliminar-inmueble/<int:inmueble_id>/',
         eliminar_inmueble, name='eliminar_inmueble'),
    path('visualizar-mensaje/<int:id>/<int:inmueble_id>/',
         visualizar_mensaje, name='visualizar_mensaje'),
    path('password-change/', CustomPasswordChangeView.as_view(),
         name='password_change'),
    path('password_change/success/', CustomPasswordChangeDoneView.as_view(),
         name='password_change_success'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
