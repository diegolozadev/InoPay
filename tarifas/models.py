from django.db import models

# Create your models here.

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
    
    
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del Servicio")
    unidad_negocio = models.CharField(max_length=50, choices=UNIDADES_NEGOCIO, verbose_name="Unidad de Negocio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    
    class Meta:
        verbose_name = "Tarifa"
        verbose_name_plural = "Tarifas"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"