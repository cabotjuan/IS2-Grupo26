from django.shortcuts import render, get_object_or_404
from .models import Propiedad
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.urls import path
from django.urls import reverse_lazy
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView, LogoutView

from HomeSwitchHome import forms

# Create your views here.

def home(request):
	return render(request, 'HomeSwitchHome/home.html',{})


def administracion(request):
	propiedades = Propiedad.objects.all()
	if request.user.is_authenticated:
		template = 'HomeSwitchHome/administracion.html'
		return render(request, template, {'propiedades':propiedades})
	else:
		return redirect(reverse_lazy('InicioAdmin'))
	
def agregar_propiedad(request):
	form = forms.PropiedadForm(request.POST or None)
	if request.method == 'GET':
		return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form})
	else:
		if form.is_valid():
			form.save()
			return redirect(reverse_lazy('administracion'))

def modificar_propiedad(request, id):
	prop = get_object_or_404(Propiedad, id=id)
	form = forms.PropiedadForm(request.POST or None, instance=prop)

	if request.method == 'GET':
		return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form})
	else:
		if form.is_valid():
			prop = form.save()
			return redirect(reverse_lazy('administracion'))
		else:
			return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form,
				'error':'Error al Actualizar propiedad.'})

class RegistroUsuario (CreateView):
	model= User
	template_name= "HomeSwitchHome/admin_formulario.html"
	form_class = UserCreationForm
	success_url=reverse_lazy('administracion')

	def form_valid(self, form):
		form.save()
		usuario = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		usuario = authenticate(username=usuario, password=password)
		login(self.request, usuario)
		return redirect(reverse_lazy('administracion'))

class Login (LoginView):
	# template_name="HomeSwitchHome/admin_formulario.html"
	# form_class=AuthenticationForm
	# success_url=reverse_lazy('administracion')

	# def dispatch(self, request, *args, **kwargs):
	# 	if request.user.is_authenticated:
	# 		return HttpResponseRedirect(self.get_success_url())
	# 	else:
	# 		return super(Login,self).dispatch(request, *args, **kwargs)

    template_name = 'HomeSwitchHome/admin_formulario.html'

class Logout(LogoutView):
    pass