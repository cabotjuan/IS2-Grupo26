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
	path('', views.home, name='home'),
    path('administracion/listado_prop', views.listado_prop, name='listado_prop'),
    path('administracion/propiedad/<id>', views.propiedad, name='prop'),
    path('administracion/agregar_propiedad', views.agregar_propiedad, name='agregar_prop'),
    path('administracion/modificar_propiedad/<id>', views.modificar_propiedad, name='modificar_prop'),
    path('administracion/registrar', views.RegistroAdmin.as_view(), name= 'RegistroAdmin'),
    #path('administracion/registrarUsuario', views.RegistroUsuario.as_view(), name= 'RegistroUser'),
    path('administracion/iniciarsesion', views.Login.as_view(), name= 'InicioAdmin'),
    #path('administracion/iniciar_sesion_usuario', views.Login.as_view(), name= 'InicioUser'),
 #    url(r'^', views.home, name = 'home'),
	path('administracion/cerrarsesion', views.Logout.as_view(), name='salir'),
 	path('administracion/', views.administracion, name='administracion'),
 	path('administracion/eliminarpropiedad/<id>', views.eliminar_propiedad, name='eliminar_propiedad'),
    path('administracion/propiedad/<id>/listado_sem', views.listado_sem, name='listado_sem'),
    path('administracion/propiedad/<id>/cerrar_subasta', views.cerrar_subasta, name='cerrar_subasta'),
    path('administracion/determinarganador/<id>', views.determinar_ganador, name='determinar_ganador'),
    path('subastasactivas', views.ver_subastas_activas, name= 'subastas_activas'),
    path('ingresarsubasta/<id>', views.ingresar_subasta, name= 'ingresar_subasta'),
    path('propiedad/<id>', views.ver_prop, name='ver_prop'),
    path('cuadrillaprop', views.ver_cuadrilla_propiedades, name= 'cuadrilla_prop'),
    path('cuadrillaprop/porzona/<zona>', views.ver_cuadrilla_x_zona, name= 'cuadrilla_prop_por_zona'),
    path('cuadrillaprop/buscar_x_zona', views.buscar_x_zona, name='buscar_x_zona'),
    path('cuadrillaprop/porfecha', views.buscar_x_fecha, name='buscar_x_fecha'),
   # path('propiedadesacotado', views.prop_acotado, name='prop_acotado')




    #path('administracion/propiedad/<id>/generarsemanas', views.generar_semanas, name='generar_semanas')
]
urlpatterns += staticfiles_urlpatterns()

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)