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
from .fechas import get_start_end_dates, monthdelta
from datetime import date, datetime
from django.contrib.auth.views import LoginView, LogoutView
from HomeSwitchHome import forms
from django.forms import modelformset_factory
from django.template import RequestContext
from django.contrib import messages
from django.db import models
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

def generar_semanas (request, id): #### ID??? ####

	### ENGANCHE DE SEMANA CON PROPIEDAD CON ID? ###
	### NUMERO DEL AÑO ELEGIDO POR EL ADMIN ###
	p= Propiedad.objects.get(id=id)

	if request.method == 'POST':
		año = int(request.POST.get('año'))
		print(año)
		for i in range(1,53):
			Semana.objects.create(propiedad= p, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(año, i))[0], fecha_fin_sem=(get_start_end_dates(año, i))[1])
		messages.success(request, "Semanas generadas!")
		return redirect(reverse_lazy('prop', kwargs= {'id':id}))
	else:
		existe2019=Semana.objects.filter(propiedad=p, fecha_inicio_sem__year=2019).exists()
		existe2020=Semana.objects.filter(propiedad=p, fecha_inicio_sem__year=2020).exists()

		return render(request, 'HomeSwitchHome/generar_semanas.html', {'existe2019':existe2019,'existe2020':existe2020,}) ### RENDER PARA BOTONES DE ELECCION DE AÑO ###



# def habilitar_sem_reserva (request, id): #### ID??? ####

	

# 	Semana.objects.filter(id=id).update()	############


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
			# for i in range(1,53):
			# 	Semana.objects.create(propiedad= form, monto_base= 0, costo=0, numero_semana=i, fecha_inicio_sem=(get_start_end_dates(2019, i))[0], fecha_fin_sem=(get_start_end_dates(2019, i))[1])
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

def borrar_fotos(request, id):
	prop = Propiedad.objects.get(id=id)
	fotos = Foto.objects.filter(propiedad=prop)
	for f in fotos:
		f.delete()
	messages.success(request,'Fotos eliminadas.')
	return redirect(reverse_lazy('modificar_prop',kwargs={'param': param}))


def abrir_subastas(request):
	ct=0
	if request.method == 'POST':
		monto = request.POST.get('monto')		
		semanas = Semana.objects.all()
		for sem in semanas:
			delta = monthdelta(sem.fecha_creacion,date.today())
			if delta >=6 and sem.habilitada:
				print('INGRESA')
				ct+=1
				propiedad = Propiedad.objects.get(id=sem.propiedad_id)
				propiedad.subastas_activas+=1
				propiedad.save()
				sem.monto_base = monto
				sub = Subasta.objects.create(fecha_inicio = date.today(), fecha_inicio_sem=sem.fecha_inicio_sem)
				sem.subasta = sub
				sem.habilitada = False
				sem.save()
		messages.success(request,'Se abrieron '+str(ct)+' Subastas.')
		return redirect(reverse_lazy('administracion'))
	return render(request,'HomeSwitchHome/abrir_subastas.html',{})

def cerrar_subastas(request):
	ct=0
	subastas = Subasta.objects.all()
	for sub in subastas:
		delta = date.today()-sub.fecha_inicio
		if delta.days >= 3:
			print('INGRESA')
			ct+=1
			hay_postores = Postor.objects.filter(subasta=sub).exists()
			if not hay_postores:
				messages.info(request,'No se encontró ganador válido(No hay postores).')
			else:
				ganador_valido = False
				while hay_postores and not ganador_valido:
					ultpostor = Postor.objects.filter(subasta=sub).latest('fecha_puja')
					ultpostor_perfil = Perfil.objects.get(usuario_id=ultpostor.usuario_id)
					tiene_reservas = Reserva.objects.filter(usuario_id=ultpostor.usuario_id, fecha_reserva=sub.fecha_inicio_sem).exists()
					if not tiene_reservas and ultpostor_perfil.creditos >= 1:
						ganador_valido = True
					else:
						ultpostor.delete()
						hay_postores = Postor.objects.filter(subasta=sub).exists()
				if ganador_valido:
					Reserva.objects.create(usuario_id=ultpostor.usuario_id,fecha_reserva=sub.fecha_inicio_sem)
				else:
					messages.info(request,'No se encontró ganador válido (Creditos insuficientes/Reservas Activas).')
				sub.delete()
	if ct:
		messages.success(request,'Se Cerraron '+str(ct)+' Subastas.')
	else:
		messages.info(request,'No hay subastas para cerrar.')

	return redirect(reverse_lazy('administracion'))


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

def buscar_x_fecha(request):
	##################### REVISAR FECHAS DEL POST ###############################

	if request.method == 'POST':
		fecha1= datetime.strptime(request.POST.get('f1'), '%Y-%m-%d').date()
		fecha2= datetime.strptime(request.POST.get('f2'), '%Y-%m-%d').date()
		if  (fecha2>fecha1) and (monthdelta(fecha1,fecha2) <= 2) and (monthdelta(date.today(),fecha1) >= 6 ) : 	
			listado_res = Semana.objects.filter(fecha_inicio_sem__range= (fecha1,fecha2)).select_related('propiedad')
			if not request.user.is_authenticated:
				listado_res = listado_res[:5]
			return render (request, 'HomeSwitchHome/cuadrilla_prop.html',{'propiedades':listado_res})
		else:

			if (fecha2<fecha1):

				messages.error(request, 'La fecha de fin del rango debe ser posterior a la fecha de inicio')
			elif (monthdelta(fecha1,fecha2) > 2):

				messages.error(request, 'El rango entre fechas no debe superar los dos meses')

			else:
				messages.error(request, 'La busqueda debe ser para al menos dentro de 6 meses')
			return render (request, 'HomeSwitchHome/buscar_x_fecha.html',{})
			#return render (request, 'HomeSwitchHome/',{}) ### ADVERTIR RANGO MAYOR A 2 MESES O BUSQUEDA MENOR A 6 MESES ###

	else:

		return render (request, 'HomeSwitchHome/buscar_x_fecha.html',{})

def buscar_x_zona (request):
	listado_zonas= Propiedad.objects.values('localidad').distinct()
	return render (request, 'HomeSwitchHome/buscar_x_zona.html',{'zonas':listado_zonas})

def  ver_cuadrilla_x_zona (request, zona):
	listado_res = Propiedad.objects.filter(localidad = zona)
	if not request.user.is_authenticated:
				listado_res = listado_res[:5]
	return render (request, 'HomeSwitchHome/cuadrilla_prop.html',{'propiedades':listado_res})

	##################### REVISAR LOCALIDAD DEL POST ###############################

	# if request.method == 'POST':

	# 	# <input type='ra'>

	# 	listado_res = Propiedad.objects.filter(localidad = zona)
	# 	return render (request, 'HomeSwitchHome/cuadrilla_prop.html',{'listado_res_prop':listado_res})


	# else:

	# 	listado_zonas= Propiedad.objects.values('localidad').distinct()
	# 	return render (request, 'HomeSwitchHome/buscar_x_zona.html',{'zonas':listado_zonas})


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
	if not request.user.is_authenticated:
		propiedades = propiedades[:5]
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
