from django.db import models
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth.models import User

# Create your models here.

# Modelo para representar las tarifas de los servicios médicos
class Tarifa(models.Model):
    
    UNIDADES_NEGOCIO = [
        ("SERVICIO MEDICO", "Servicio Médico"),
        ("INTERCONSULTA", "Interconsulta"),
        ("LAB. PULMONAR", "Laboratorio Pulmonar"),
        ("CLINICA DE ALERGIAS", "Clínica de Alergias"),
        ("CLINICA DE SUEÑO", "Clínica de Sueño"),
        ("PROCEDIMIENTOS", "Procedimientos"),
        ("PROGRAMAS INTEGRALES", "Programas Integrales"),
        ("INVESTIGACIÓN", "Investigación")
    ]
    
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    precio = models.PositiveIntegerField(verbose_name="Precio del Servicio")
    unidad_negocio = models.CharField(max_length=50, choices=UNIDADES_NEGOCIO, verbose_name="Unidad de Negocio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"

    def __str__(self):
        return f"{self.nombre} - ${intcomma(self.precio)} ({self.unidad_negocio})"