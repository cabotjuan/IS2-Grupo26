from django.shortcuts import render
from .models import Propiedad
# Create your views here.

def home(request):
	#propiedades = Propiedad.objects.all()
	return render(request, 'HomeSwitchHome/home.html',{})