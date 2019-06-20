from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from HomeSwitchHome.models import Propiedad, Foto, Postor, Perfil, Tarjeta
from django.core.exceptions import NON_FIELD_ERRORS
from datetime import date

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

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email',]

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')

# class UserForm(UserCreationForm):
# 	  email = forms.EmailField(required=True, unique=True)
# 	  class Meta:
# 		model = User 
# 	  	fields = ["username", "email", "password1", "password2"]


class PerfilForm(ModelForm):
	class Meta:
		model = Perfil
		fields = [
			'nombre',
			'apellido',
			'fecha_nacimiento'
		]
		widgets = {'fecha_nacimiento': forms.DateInput(format=('%Y/%m/%d'), attrs={'class':'form-control', 'placeholder':'Seleccionar', 'type':'date'}),
		}


	def clean_fecha_nacimiento(self):
		fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
		today = date.today()
		age = today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
		if age < 18: 
			raise forms.ValidationError('ERROR. El usuario es menor de edad.')
		else:
			return fecha_nacimiento
class TarjetaForm(ModelForm):
	class Meta:
		model = Tarjeta
		fields = [
			'nro_tarjeta',
			'marca',
			'titular',
			'm_vencimiento',
			'a_vencimiento', 
			'cod_seguridad' 
		]
	def clean_a_vencimiento(self):
		a_vencimiento = self.cleaned_data.get('a_vencimiento')
		today = date.today()
		if a_vencimiento < today.year: 
			raise forms.ValidationError('ERROR. Tarjeta Vencida.')
		else:
			return a_vencimiento

	def clean_m_vencimiento(self):
		m_vencimiento = self.cleaned_data.get('m_vencimiento')
		today = date.today()
		if self.cleaned_data.get('a_vencimiento') == today.year: 
			if m_vencimiento < today.month: 
				raise forms.ValidationError('ERROR. Tarjeta Vencida.')
		else:
			return m_vencimiento