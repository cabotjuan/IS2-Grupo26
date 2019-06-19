from django.db import models
from datetime import date, timezone
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# Create your models here.

class Propiedad(models.Model):
	titulo = models.CharField(max_length=30)
	descripcion = models.TextField()
	pais = models.CharField(max_length=20)
	provincia = models.CharField(max_length=20)
	localidad = models.CharField(max_length=30)
	direccion = models.CharField(max_length=40)
	subastas_activas = models.IntegerField(default=0)
	def __str__(self):
		return self.titulo
	class Meta:
		unique_together = ("titulo", "localidad")
	

class Semana(models.Model):
	propiedad = models.ForeignKey('Propiedad', on_delete=models.CASCADE)
	subasta = models.OneToOneField('Subasta', null=True, on_delete=models.SET_NULL)
	reserva = models.OneToOneField('Reserva', null=True, on_delete=models.SET_NULL)
	monto_base = models.FloatField(blank=True)
	costo = models.FloatField(blank=True)
	numero_semana = models.IntegerField(blank=True)
	fecha_inicio_sem = models.DateField(blank=True)
	fecha_fin_sem = models.DateField(blank=True)
	habilitada = models.BooleanField(default=True)

class Reserva(models.Model):
	usuario = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	fecha_reserva = models.DateField(blank=True)

class Subasta(models.Model):
	usuario = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	fecha_inicio = models.DateField(blank=True)
	fecha_fin = models.DateField(blank=True)

class Postor(models.Model):
	usuario = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	subasta = models.ForeignKey('Subasta', on_delete=models.CASCADE)	
	monto_puja = models.FloatField()	
	fecha_puja = models.DateTimeField(default=timezone.now)
	class Meta:
		order_with_respect_to = 'fecha_puja'	

class Foto(models.Model):
	archivo = models.ImageField(blank=True, null=True, upload_to='images/')
	propiedad = models.ForeignKey('Propiedad', on_delete= models.CASCADE)


class Perfil(models.Model):
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	nombre = models.CharField(max_length=20)
	apellido = models.CharField(max_length=20)
	fecha_nacimiento = models.DateField()
	creditos = models.IntegerField(default=2)
	es_premium = models.BooleanField(default=False)

class Tarjeta(models.Model):
	TARJETAS_DISP = [('VISA', 'VISA'),('MASTERCARD', 'MASTERCARD')]
	usuario = models.OneToOneField(User, on_delete=models.CASCADE)
	nro_tarjeta = models.IntegerField(primary_key=True)
	marca = models.CharField(choices=TARJETAS_DISP, max_length=10) 
	titular = models.CharField(max_length=20)
	m_vencimiento = models.SmallIntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)])
	a_vencimiento = models.SmallIntegerField(validators=[MinValueValidator(2019),MaxValueValidator(2100)])
	cod_seguridad = models.SmallIntegerField()
