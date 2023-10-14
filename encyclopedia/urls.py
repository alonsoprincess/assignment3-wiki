from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entryTitle>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newPage/", views.newPage, name="newPage"),
    path("edit/<str:entryTitle>", views.edit, name="edit"),
    #path("savePage/", views.savePage, name="savePage"),
    path("randomize/", views.randomize, name="randomize")
]
