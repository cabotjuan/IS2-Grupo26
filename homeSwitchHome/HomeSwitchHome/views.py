from django.shortcuts import render, get_object_or_404
from .models import Propiedad, Semana, Subasta
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
from . import fechas
from .fechas import get_start_end_dates


from django.contrib.auth.views import LoginView, LogoutView

from HomeSwitchHome import forms

# Create your views here.

def home(request):
	return render(request, 'HomeSwitchHome/home.html',{})

def listado_prop(request):
	propiedades = Propiedad.objects.all()
	template = 'HomeSwitchHome/listado_prop.html'
	return render(request, template, {'propiedades':propiedades})
	

def administracion(request):
	if request.user.is_authenticated:
		template = 'HomeSwitchHome/administracion.html'
		return render(request, template, {})
	else:
		return redirect(reverse_lazy('InicioAdmin'))


def propiedad(request, id):
	p = Propiedad.objects.get(id=id)
	return render(request, 'HomeSwitchHome/propiedad.html',{'Propiedad':p})
	
def agregar_propiedad(request):

	form = forms.PropiedadForm(request.POST or None)
	if request.method == 'GET':
		return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form})
	else:
		if form.is_valid():
			p = form.save()

			for i in range(1,53):
				Semana.objects.create(propiedad= p, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
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