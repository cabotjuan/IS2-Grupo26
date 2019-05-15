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

# Create your views here.

def home(request):
	#propiedades = Propiedad.objects.all()
	return render(request, 'HomeSwitchHome/home.html',{})


class RegistroUsuario (CreateView):
	model= User
	template_name= "HomeSwitchHome/admin_formulario.html"
	form_class=UserCreationForm

class Login (FormView):
	template_name="HomeSwitchHome/admin_formulario.html"
	form_class=AuthenticationForm
	success_url=reverse_lazy('home')

	def dispatch(self, request, *args, **kwargs):
		if request.user.is_authenticated:
			return HttpResponseRedirect(self.get_success_url())
		else:
			return super(Login,self).dispatch(request, *args, **kwargs)


def logout (request):
	logout(request) 