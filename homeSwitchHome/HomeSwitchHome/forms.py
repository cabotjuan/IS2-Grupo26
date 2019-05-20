from django import forms
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

class ImageForm(ModelForm):
	archivo = forms.ImageField(label='archivo')
	class Meta:
		model = Foto
		fields = ('archivo',)

class PostorForm(ModelForm):
	class Meta:
		model = Postor
		fields = [
			'mail',
			'monto_puja'
		]