from django.shortcuts import render, get_object_or_404
from .models import Propiedad, Semana, Subasta, Foto, Postor
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
from HomeSwitchHome import forms
from django.forms import modelformset_factory
from django.template import RequestContext
from django.contrib import messages
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

def ver_prop(request, id):
	p = Propiedad.objects.get(id=id)
	return render(request, 'HomeSwitchHome/ver_prop.html',{'Propiedad':p})

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
	Imageformset = modelformset_factory(Foto, form= forms.ImageForm ,min_num=0, max_num=5,extra=5)
	

	if request.method == 'GET':

		form = forms.PropiedadForm()
		formset = Imageformset(queryset=Foto.objects.none())
		return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form, 'formset':formset})
	else:

		### POST ###

		form = forms.PropiedadForm(request.POST)
		formset = Imageformset(request.POST, request.FILES, queryset=Foto.objects.none())

		if form.is_valid() and formset.is_valid():
			form = form.save(commit = False)
			form.save()
			file_list = [i for i in formset.cleaned_data if i]
			print('LISTA: ---------------') 
			print(file_list) 
			for f in file_list:
				archivo = f['archivo']
				foto = Foto(archivo=archivo, propiedad=form)
				foto.save()
				#messages.success(request, "Guardado!")
			for i in range(1,53):
				Semana.objects.create(propiedad= form, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
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

def determinar_ganador(request, id):	

	sub = Subasta.objects.get(id=id)
	print('HOLAAAA')
	print(sub.id)
	hay_ganador = Postor.objects.filter(subasta=sub).exists()
	if hay_ganador:
		ganador = Postor.objects.filter(subasta=sub).latest('fecha_puja')
	else:
		ganador = None
	Subasta.objects.filter(id=id).delete()
	return render(request, 'HomeSwitchHome/determinar_ganador.html',{'ganador':ganador})

def cerrar_subasta(request, id):

	listado_hab = Semana.objects.filter(propiedad=id).filter(habilitada = False).filter(subasta_id__isnull=False)
	############################################### CERRAR SUBASTA . BORRA LA SUBASTA y disminuye cant subastas #########################################
	if request.method == 'POST':
		propiedad = Propiedad.objects.get(id=id)
		nro = request.POST.get('semana')
		sem = listado_hab.get(numero_semana= nro)
		subasta = sem.subasta
		propiedad.subastas_activas-=1
		propiedad.save()
		return redirect(reverse_lazy('administracion')+'determinarganador/'+str(subasta.id))
	else:
		return render(request, 'HomeSwitchHome/cerrar_subasta.html', {'listado_hab':listado_hab})

def ver_cuadrilla_propiedades(request):

	propiedades= Propiedad.objects.all()
	template = 'HomeSwitchHome/cuadrilla_prop.html'
	return render(request, template, {'propiedades':propiedades})

def ver_subastas_activas(request):
	semanas= Semana.objects.exclude(subasta_id__isnull = True)
	template = 'HomeSwitchHome/subastas_activas.html'
	return render(request, template, {'semanas':semanas})


def ingresar_subasta(request, id):
	subasta=Subasta.objects.get(id=id)
	semana = Semana.objects.get(subasta=subasta)
	print('------------')
	print(subasta.id)
	print(semana.subasta.id)
	print('------------')
	args={}
	if request.method == 'POST':
		form = forms.PostorForm(request.POST)
		
		if form.is_valid(): 
			print('Formulario Valido')
			monto_puja = float(request.POST.get('monto_puja'))
			if Postor.objects.count() > 0:
				ultpostor = Postor.objects.latest('fecha_puja')
				if monto_puja > ultpostor.monto_puja:
					f = form.save(commit=False)
					f.subasta = subasta
					f.save() 
			else:
				f = form.save(commit=False)
				f.subasta = subasta
				f.save()
		else:
			print('formulario invalido!')
		return redirect(reverse_lazy('home'))
	else:
		form = forms.PostorForm()
		if Postor.objects.count() > 0:
			args={'form':form,'semana':semana, 'monto_mas_alto':(Postor.objects.latest('fecha_puja')).monto_puja}
		else:
			args={'form':form,'semana':semana}
		return render(request, 'HomeSwitchHome/ingresar_subasta.html', args)

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