from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("connexion/", views.auth_login_view, name="login"),
    path("deconnexion/", views.auth_logout_view, name="logout"),
    path("auth/google/", views.google_login_view, name="google_login"),
    path("auth/google/callback/", views.google_callback_view, name="google_callback"),
]
