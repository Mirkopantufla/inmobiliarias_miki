from django.urls import path, include
from .views import indice, register, logout_view, profile, update_profile, acerca, contacto, CustomPasswordChangeView, CustomLoginView, CustomPasswordChangeDoneView
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns = [
    path('', indice, name='indice'),
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('acerca/', acerca, name='acerca'),
    path('contacto/', contacto, name='contacto'),
    path('update_profile/', update_profile, name='update_profile'),
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
