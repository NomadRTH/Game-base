from django.urls import path 
from . import views

app_name = "games"

urlpatterns = [
    path('', views.index, name = "index"),
    path("<int:game_id>/", views.detail, name="detail"),
    path("register/", views.register, name="register"),
    path("person/", views.person, name="person"),
    path("<int:game_id>/add_review/", views.add_review, name="add_review"),
    path("review/<int:review_id>/delete/", views.delete_review, name="delete_review"),

]   