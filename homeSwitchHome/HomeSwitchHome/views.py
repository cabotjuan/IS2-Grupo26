from django.shortcuts import render, get_object_or_404
from .models import Propiedad, Semana, Subasta, Foto 
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
from datetime import date
from django.contrib.auth.views import LoginView, LogoutView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from HomeSwitchHome import forms
from django.forms import modelformset_factory
# Create your views here.

def home(request):
	return render(request, 'HomeSwitchHome/home.html',{})

def listado_prop(request):
	propiedades = Propiedad.objects.all()
	template = 'HomeSwitchHome/listado_prop.html'
	return render(request, template, {'propiedades':propiedades})
	

def administracion(request):
		template = 'HomeSwitchHome/administracion.html'
		return render(request, template, {})

def propiedad(request, id):
	p = Propiedad.objects.get(id=id)
	return render(request, 'HomeSwitchHome/propiedad.html',{'Propiedad':p})

	
def eliminar_propiedad(request, id):
	p= Propiedad.objects.get(id=id)
	p.delete()
	return redirect(reverse_lazy(listado_prop))
	
# class AgregarPropiedad(CreateWithInlinesView):
# 	template_name = 'HomeSwitchHome/agregar_propiedad.html'
# 	model = Propiedad
# 	form_class = forms.PropiedadForm
# 	inlines = [forms.FotosInline,]
# 	success_url = reverse_lazy('administracion')

# 	def form_valid(self, form):
# 		p = form.save()
# 		for i in range(1,53):
# 			Semana.objects.create(propiedad= p, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
# 		return redirect(reverse_lazy('administracion'))

def agregar_propiedad(request):
#	Imageformset = modelformset_factory(Foto, fields=('archivo','propiedad'),extra=5)
	form = forms.PropiedadForm(request.POST or None)

	if request.method == 'GET':
#		formset = Imageformset(queryset=Foto.objects.none())
		return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form})
	else:
#		formset = Imageformset(request.POST, request.FILES)
		if form.is_valid():
			p = form.save()
#			for f in formset:
#				foto = Foto(archivo=f.cleaned_data.get('archivo'), propiedad=p)
#				foto.save()
			for i in range(1,53):
				Semana.objects.create(propiedad= p, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
			return redirect(reverse_lazy(administracion))


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

def listado_sem(request, id):
	listado= Semana.objects.filter(fecha_inicio_sem__gte= date.today()).filter(propiedad=id)
	############################################### GUARDAR SEMANA Y CREAR SUBASTA #########################################
	if request.method == 'POST':
		propiedad = Propiedad.objects.get(id=id)
		
		propiedad.subastas_activas+=1
		propiedad.save()
		nro = request.POST.get('semana')
		monto = request.POST.get('monto')
		print('NUMERO:   '+nro)
		print('MONTO:    '+monto)
		sem = listado.get(numero_semana= nro)
		print('SEMANA:  '+str(sem.numero_semana))
		print('SEMANA inicia:  '+str(sem.fecha_inicio_sem))
		print('SEMANA fin:  '+str(sem.fecha_fin_sem))
		sem.monto_base = monto
		sub = Subasta.objects.create(fecha_inicio = sem.fecha_inicio_sem,fecha_fin = sem.fecha_fin_sem)
		sem.subasta = sub
		sem.habilitada = False
		sem.save()
		return redirect(reverse_lazy('administracion')+'propiedad/'+id)
	else:
		return render(request, 'HomeSwitchHome/listado_sem.html', {'listado':listado})	

def cerrar_subasta(request, id):

	listado_hab = Semana.objects.filter(propiedad=id).filter(habilitada = False)
	############################################### CERRAR SUBASTA . BORRA LA SUBASTA y disminuye cant subastas #########################################
	if request.method == 'POST':
		propiedad = Propiedad.objects.get(id=id)


		nro = request.POST.get('semana')
		sem = listado_hab.get(numero_semana= nro)
		subasta = sem.subasta
		print(subasta.id)
		Subasta.objects.filter(id=subasta.id).delete()
		
		propiedad.subastas_activas-=1
		propiedad.save()

		return redirect(reverse_lazy('administracion')+'propiedad/'+id)
	else:
		return render(request, 'HomeSwitchHome/cerrar_subasta.html', {'listado_hab':listado_hab})	

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