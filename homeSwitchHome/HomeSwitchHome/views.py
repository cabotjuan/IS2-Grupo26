from django.shortcuts import render
from .models import Propiedad
# Create your views here.

def home(request):
	return render(request, 'HomeSwitchHome/home.html',{})

def administracion(request):
	#if request.user.is_authenticated
	return render(request, 'HomeSwitchHome/administracion.html', {})
	#else
	#	return render(request, 'HomeSwitchHome/login.html',{})

def Prop_list(request):
	propiedades = Propiedad.objects.all()
	return render(request, 'HomeSwitchHome/prop_list.html', {'propiedades':propiedades})

def agregar_propiedad(request):
	return render(request, 'HomeSwitchHome/agregar_propiedad.html')