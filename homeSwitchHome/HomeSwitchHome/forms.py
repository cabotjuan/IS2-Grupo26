from django.forms import ModelForm
from HomeSwitchHome.models import Propiedad, Foto, Postor

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


class PostorForm(ModelForm):
	class Meta:
		model = Postor
		fields = [
			'mail',
			'monto_puja'
		]