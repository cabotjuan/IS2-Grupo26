from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Propiedad, Semana, Subasta, Foto, Postor, Perfil, Tarjeta
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
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
	messages.success(request, 'Propiedad eliminada.')
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
		#return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form, 'formset':formset})
	else:

		### POST ###

		form = forms.PropiedadForm(request.POST)
		formset = Imageformset(request.POST, request.FILES, queryset=Foto.objects.none())

		if form.is_valid() and formset.is_valid():
			print('Form OK')
			form = form.save(commit = False)
			form.save()
			file_list = [i for i in formset.cleaned_data if i]
			for f in file_list:
				archivo = f['archivo']
				foto = Foto(archivo=archivo, propiedad=form)
				foto.save()
			for i in range(1,53):
				Semana.objects.create(propiedad= form, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
			messages.success(request, "Propiedad Agregada!")
			return redirect(reverse_lazy(administracion))

		else:
			print('Form Error')
	return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form, 'formset':formset})


def modificar_propiedad(request, id):
	Imageformset = modelformset_factory(Foto, form= forms.ImageForm ,min_num=0, max_num=5,extra=5)
	prop = get_object_or_404(Propiedad, id=id)
	form = forms.PropiedadForm(request.POST or None, instance=prop)
	fotos = Foto.objects.filter(propiedad=prop)
	formset = Imageformset(queryset=fotos)

	if request.method == 'POST':
		formset = Imageformset(request.POST,request.FILES, queryset=Foto.objects.filter(propiedad=prop))

		
		print('VALIDACION form:')
		print(form.is_valid())
		print('VALIDACION formset:')
		print(formset.is_valid())

		if form.is_valid() and formset.is_valid():
			print('Form OK!')
			
			form = form.save(commit = False)
			form.save()

			Foto.objects.filter(propiedad=prop).delete()
			
			#if hasattr(formset, 'deleted_objects'):
			#	for obj in formset.deleted_objects:
			#		obj.delete() 
			file_list = [i for i in formset.cleaned_data if i]
			print('FILELIST',file_list)
			for f in file_list:
			 	archivo = f['archivo']
			 	foto = Foto(archivo=archivo, propiedad=form)
			 	foto.save()

			messages.success(request, 'Propiedad modificada!')
			return redirect(reverse_lazy('administracion'))
		else:
			messages.success(request, 'La propiedad no se ha modificado.')
			return redirect(reverse_lazy('administracion'))

	return render(request, 'HomeSwitchHome/agregar_propiedad.html', {'form':form, 'formset':formset})






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
				ultpostor = Postor.objects.filter(subasta=subasta).latest('fecha_puja')
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

#perfil = Perfil.objects.get(usuario=request.user)
#tarjeta = Tarjeta.objects.get(usuario=request.user)
def RegistroUsuario(request):
	if request.method == 'POST':
		user_form = forms.UserForm(request.POST, prefix="user_form")
		perfil_form = forms.PerfilForm(request.POST, prefix="perfil_form")
		tarj_form = forms.TarjetaForm(request.POST, prefix="tarj_form")
		print('-------------')
		print(user_form.is_valid())
		print(perfil_form.is_valid())
		print(tarj_form.is_valid())
		print('-------------')
		if user_form.is_valid() and perfil_form.is_valid() and tarj_form.is_valid():
			u = user_form.save(commit= False)
			p = perfil_form.save(commit=False)
			t = tarj_form.save(commit=False)
			u.username = u.email
			u.is_staff = False
			u.is_superuser = False
			u.save()
			u = User.objects.get(username=u.email)
			p.usuario_id = u.id
			t.usuario_id = u.id 
			p.save()
			t.save()
			password = user_form.cleaned_data.get('password1')
			usuario = authenticate(username=u, password=password)
			login(request, usuario)
			messages.success(request, 'Perfil Creado con exito!')
			return redirect('home')
		else:
			return render(request, 'HomeSwitchHome/user_auth.html', {
			'user_form': user_form,
			'perfil_form': perfil_form,
			'tarj_form': tarj_form
			})

			#messages.error(request, 'Datos Incorrectos.')
			#return redirect('RegistroUser')
	else:
		user_form = forms.UserForm(prefix="user_form")
		perfil_form = forms.PerfilForm(prefix="perfil_form")
		tarj_form = forms.TarjetaForm(prefix="tarj_form")
		return render(request, 'HomeSwitchHome/user_auth.html', {
		'user_form': user_form,
		'perfil_form': perfil_form,
		'tarj_form': tarj_form
})


class RegistroAdmin (CreateView):
	model= User
	template_name= "HomeSwitchHome/admin_auth.html"
	form_class = UserCreationForm
	success_url=reverse_lazy('administracion')

	def form_valid(self, form):
		u = form.save(commit=False)
		u.is_staff = True
		u.is_superuser = True
		u.save()
		usuario = form.cleaned_data.get('username')
		password = form.cleaned_data.get('password1')
		usuario = authenticate(username=usuario, password=password)
		login(self.request, usuario)
		return redirect(reverse_lazy('administracion'))

def userLogin(request):
	if request.method == 'POST': 
		form = AuthenticationForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				# Redirect to a successpage
				return redirect(reverse_lazy('home'))
			else:
				messages.error(request, 'Cuenta deshabilitada.')
		else:
			messages.error(request, 'Mail o contraseña Incorrecta.')
	else:
		form = AuthenticationForm()
	return render(request,"HomeSwitchHome/iniciar_sesion.html",{'form':form})


def userLogout(request):
	logout(request)
	return redirect(reverse_lazy('home'))
class Login (LoginView):
	template_name = 'HomeSwitchHome/admin_auth.html'
class Logout(LogoutView):
	pass



def verPerfil(request):
	print(request.user.id)
	perfil = Perfil.objects.get(usuario=request.user.id)
	tarjeta = Tarjeta.objects.get(usuario=request.user.id)
	return render(request, 'HomeSwitchHome/mi_perfil.html', {'usuario': request.user,'perfil':perfil,'tarjeta':tarjeta})
	


def editarPerfil(request, id):
	user = User.objects.get(id=id)
	perfil = Perfil.objects.get(usuario=id)
	tarjeta = Tarjeta.objects.get(usuario=id)
	user_form = forms.UserForm(request.POST or None, instance=user, prefix="user_form")
	perfil_form = forms.PerfilForm(request.POST or None, instance=perfil, prefix="perfil_form")
	tarj_form = forms.TarjetaForm(request.POST or None, instance=tarjeta, prefix="tarj_form")
	#mail = user_form.cleaned_data.get('email')
	if request.method == 'POST':
		if user_form.is_valid() and perfil_form.is_valid() and tarj_form.is_valid():
			messages.success(request,'Perfil Actualizado Correctamente.')
			user_form.save()
			perfil_form.save()
			tarj_form.save()
			usuario = user_form.cleaned_data.get('email')
			password = user_form.cleaned_data.get('password1')
			usuario = authenticate(username=usuario, password=password)
			login(request, usuario)
			return redirect('home')
#		elif not user_form.is_valid():
#			user_form['password'].validate()
#			if mail == user_form.cleaned_data.get('email'):

	return render(request, 'HomeSwitchHome/editar_perfil.html',{'usuario':user_form,'perfil':perfil_form,'tarjeta':tarj_form})