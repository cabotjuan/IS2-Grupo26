from django import forms
from django.forms import ModelForm

from HomeSwitchHome.models import Propiedad, Foto, Postor
from django.core.exceptions import NON_FIELD_ERRORS

class PropiedadForm(ModelForm):
	class Meta:

		model = Propiedad
		fields = [
			'titulo',
			'descripcion',
			'pais',
			'provincia',
			'localidad',
			'direccion'
			]
		error_messages = {
		NON_FIELD_ERRORS: {
			'unique_together': "El titulo ya existe en esta Localidad. Por favor ingresa uno diferente.",
			}
		}

	# def clean_titulo(self):
	# 	titulo = self.cleaned_data.get('titulo')
	# 	print('clean titulo')
	# 	try:
	# 		var = Propiedad.objects.get(titulo=titulo)
	# 	except Propiedad.DoesNotExist:
	# 		var = None
	# 	if var:
	# 		raise forms.ValidationError("")		
	# 	return titulo

class ImageForm(ModelForm):
	archivo = forms.ImageField(label='archivo')
	class Meta:
		model = Foto
		fields = ('archivo',)

class PostorForm(ModelForm):
	class Meta:
		model = Postor
		fields = [
			'usuario',
			'monto_puja'
		]