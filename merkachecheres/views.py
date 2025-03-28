from django.shortcuts import render
import random
import requests
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.




def index(request):
    #return HttpResponse("Index")
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def registro(request):
    return render(request, "registro.html")

def completardatos(request):
    return render(request, "completardatos.html")