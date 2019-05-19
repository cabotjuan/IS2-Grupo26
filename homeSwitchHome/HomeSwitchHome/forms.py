from django.forms import ModelForm
from HomeSwitchHome.models import Propiedad, Foto

class PropiedadForm(ModelForm):
	class Meta:
		model = Propiedad
		fields = [
			'titulo',
			'descripcion',
			'pais',
			'provincia',
			'direccion'
			]
	
# ESTO VA EN LA VISTA. 

 	#form = PropiedadForm()

# 	#prop = Propiedad.objects.get(pk=1)
# 	#form = PropiedadForm(instance=prop)
