from django.shortcuts import render, redirect
from .models import *
from django.http import HttpResponse
from .models import UploadedImage


# Create your views here.
def home(request):
    return render(request, "index.html")


def upload_image(request):
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        UploadedImage.objects.create(image=image)
        return redirect("index")
    return redirect("index")


def index(request):
    images = UploadedImage.objects.latest("timestamp")
    return render(request, "index.html", {"images": images})
