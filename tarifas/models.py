from django.db import models

# Create your models here.

class Servicio(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio del Servicio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    
    
    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"