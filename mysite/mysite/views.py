from django.http import HttpResponse
from django.shortcuts import render

def landing_view(request):
    return render(request, "upload.html")
