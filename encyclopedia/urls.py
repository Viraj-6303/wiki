from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:var>", views.name, name="name"),
    path("search", views.search, name="search"),
    path("new", views.new, name="new" ),
    path("edit", views.edit, name="edit"),
]
