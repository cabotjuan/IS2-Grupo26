"""homeSwitchHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from HomeSwitchHome import views
from HomeSwitchHome.views import *
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [

    # USER VIEWS

	path('', views.ver_cuadrilla_propiedades, name='home'),
    path('favoritos', views.ver_fav, name='ver_fav'),
    path('quitar_fav/<id>', views.quitar_fav, name='quitar_fav'),
    path('agregar_fav/<id>', views.agregar_fav, name='agregar_fav'),
    path('registrarUsuario', views.RegistroUsuario, name= 'RegistroUser'),
    path('iniciar_sesion_usuario', views.userLogin, name= 'InicioUser'),
    path('cerrar_sesion_usuario', views.userLogout, name='SalirUser'),
    path('subastasactivas', views.ver_subastas_activas, name= 'subastas_activas'),
    path('mis_reservas', views.ver_mis_reservas, name= 'mis_reservas'),
    path('mis_subastas', views.ver_mis_subastas, name= 'mis_subastas'),
    path('ingresarsubasta/<id>', views.ingresar_subasta, name= 'ingresar_subasta'),

    path('realizarreserva/<id>', views.realizar_reserva, name= 'realizar_reserva'),
    path('confirmarreserva/<id>', views.confirmar_reserva, name= 'confirmar_reserva'),
    path('realizar_reserva_hotsale/<id>', views.realizar_reserva_hotsale, name= 'realizar_reserva_hotsale'),
    path('cancelar_reserva/<id>', views.cancelar_reserva, name= 'cancelar_reserva'),
    path('ver_cancelar_reserva/<id>', views.ver_cancelar_reserva, name= 'ver_cancelar_reserva'),
    path('propiedad/<id>', views.ver_prop, name='ver_prop'),

    path('perfil', views.verPerfil, name='perfil'),
    path('solicitar_baja', views.solicitar_baja, name='solicitar_baja'),
    path('solicitar_alta', views.solicitar_alta, name='solicitar_alta'),
    path('editar_perfil/<id>', views.editarPerfil, name='editarPerfil'),
    path('cuadrillaprop', views.ver_cuadrilla_propiedades, name= 'cuadrilla_prop'),
    path('cuadrillaprop/porzona/<zona>', views.ver_cuadrilla_x_zona, name= 'cuadrilla_prop_por_zona'),
    path('cuadrillaprop/buscar_x_zona', views.buscar_x_zona, name='buscar_x_zona'),
    path('cuadrillaprop/porfecha', views.buscar_x_fecha, name='buscar_x_fecha'),
   # path('propiedadesacotado', views.prop_acotado, name='prop_acotado')
    path('recuperarclave', views.recuperarClave, name= 'recuperar_clave'),



    # ADMIN VIEWS

    path('administracion/listado_prop', views.listado_prop, name='listado_prop'),
    path('administracion/listado_res', views.listado_prop_res, name='listado_prop_res'),
    path('administracion/listado_res/<id>', views.listado_res, name='listado_res'),
    path('administracion/propiedad/<id>', views.propiedad, name='prop'),
    path('administracion/agregar_propiedad', views.agregar_propiedad, name='agregar_prop'),
    path('administracion/modificar_propiedad/<id>', views.modificar_propiedad, name='modificar_prop'),
    path('administracion/modificar_propiedad/<id>/borrar_fotos', views.borrar_fotos, name='borrar_fotos'),
    path('administracion/registrar', views.RegistroAdmin.as_view(), name= 'RegistroAdmin'),
    path('administracion/iniciarsesion', views.Login.as_view(), name= 'InicioAdmin'),
	path('administracion/cerrarsesion', views.Logout.as_view(), name='salir'),
 	path('administracion/', views.administracion, name='administracion'),
 	path('administracion/eliminarpropiedad/<id>', views.eliminar_propiedad, name='eliminar_propiedad'),
    path('administracion/propiedad/<id>/listado_sem', views.listado_sem, name='listado_sem'),
    #path('administracion/propiedad/<id>/cerrar_subasta', views.cerrar_subasta, name='cerrar_subasta'),
    #path('administracion/determinarganador/<id>', views.determinar_ganador, name='determinar_ganador'),
    path('administracion/propiedad/<id>/generarsemanas', views.generar_semanas, name='generar_semanas'),
    path('administracion/propiedad/<id>/habilitar_reservas', views.habilitar_reservas, name='habilitar_reservas'),
    path('administracion/propiedad/<id>/habilitar_hotsales', views.habilitar_hotsales, name='habilitar_hotsale'),
    path('administracion/abrirsubastas', views.abrir_subastas, name='abrir_subastas'),
    path('administracion/cerrarsubastas', views.cerrar_subastas, name='cerrar_subastas'),
    path('administracion/usuario/<id>', views.ver_perfil_usuario, name='perfil_usuario'),
    path('administracion/listado_usuarios', views.listado_usuarios, name='listado_usuarios'),
    path('administracion/aceptar_alta/<id>', views.aceptar_alta, name='aceptar_alta'),
    path('administracion/rechazar_alta/<id>', views.rechazar_alta, name='rechazar_alta'),
    path('administracion/aceptar_baja/<id>', views.aceptar_baja, name='aceptar_baja'),
    path('administracion/rechazar_baja/<id>', views.rechazar_baja, name='rechazar_baja'),
    path('administracion/ver_solicitudes', views.ver_solicitudes, name='ver_solicitudes')
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)