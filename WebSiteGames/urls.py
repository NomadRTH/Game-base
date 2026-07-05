from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", RedirectView.as_view(url="/games/")),
    path('games/', include("games.urls")),
    path('admin/', admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="games/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
