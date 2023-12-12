from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.upload_image, name="upload_image"),
    path("index/", views.index, name="index"),
]
