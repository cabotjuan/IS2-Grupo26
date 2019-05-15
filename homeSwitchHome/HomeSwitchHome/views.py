from django.shortcuts import render
from .models import Propiedad
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.urls import path
from django.urls import reverse_lazy
from django.shortcuts import redirect

# Create your views here.

def home(request):

	return render(request, 'HomeSwitchHome/home.html',{})

def administracion(request):
	if request.user.is_authenticated:
		return render(request, 'HomeSwitchHome/administracion.html', {})
	else:
		return HttpResponseRedirect(reverse_lazy('InicioAdmin'))

def Prop_list(request):
	propiedades = Propiedad.objects.all()
	return render(request, 'HomeSwitchHome/prop_list.html', {'propiedades':propiedades})

def agregar_propiedad(request):
	return render(request, 'HomeSwitchHome/agregar_propiedad.html')
	#propiedades = Propiedad.objects.all()


class RegistroUsuario (CreateView):
	model= User
	template_name= "HomeSwitchHome/admin_formulario.html"
	form_class=UserCreationForm
	success_url=reverse_lazy('administracion')

class Login (FormView):
	template_name="HomeSwitchHome/admin_formulario.html"
	form_class=AuthenticationForm
	success_url=reverse_lazy('administracion')

	# def dispatch(self, request, *args, **kwargs):
	# 	if request.user.is_authenticated:
	# 		return HttpResponseRedirect(self.get_success_url())
	# 	else:
	# 		return super(Login,self).dispatch(request, *args, **kwargs)


def logout (request):
	logout(request) 