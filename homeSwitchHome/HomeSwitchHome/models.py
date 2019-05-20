from django.db import models
from datetime import date, timezone
from django.utils import timezone
# Create your models here.

class Propiedad(models.Model):
	titulo = models.CharField(max_length=30)
	descripcion = models.TextField()
	pais = models.CharField(max_length=20)
	provincia = models.CharField(max_length=20)
	direccion = models.CharField(max_length=40)
	subastas_activas = models.IntegerField(default=0)
	def __str__(self):
		return self.titulo


class Semana(models.Model):
	propiedad = models.ForeignKey('Propiedad', on_delete=models.CASCADE)
	subasta = models.OneToOneField('Subasta', null=True, on_delete=models.SET_NULL)
	#reserva = models.OneToOneField('Reserva', null=True, on_delete=models.DO_NOTHING)
	monto_base = models.FloatField(blank=True)
	costo = models.FloatField(blank=True)
	numero_semana = models.IntegerField(blank=True)
	fecha_inicio_sem = models.DateField(blank=True)
	fecha_fin_sem = models.DateField(blank=True)
	habilitada = models.BooleanField(default=True)
class Subasta(models.Model):
	fecha_inicio = models.DateField(blank=True)
	fecha_fin = models.DateField(blank=True)

class Postor(models.Model):
	subasta = models.ForeignKey('Subasta', on_delete=models.CASCADE)	
	mail = models.EmailField()
	monto_puja = models.FloatField()	
	fecha_puja = models.DateTimeField(default=timezone.now)
	class Meta:
		order_with_respect_to = 'fecha_puja'	

class Foto(models.Model):
	archivo = models.ImageField(blank=True, null=True, upload_to='images/')
	propiedad = models.ForeignKey('Propiedad', on_delete= models.CASCADE)