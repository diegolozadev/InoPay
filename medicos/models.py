from django.db import models

# Create your models here.

class Medico(models.Model):
    
    ESPECIALIDADES = [
        ('Neumología Adulto', 'Neumología Adulto'),
        ('Neumología Pediátrica', 'Neumología Pediátrica'),
        ('Alergología', 'Alergología'),
        ('Medicina General', 'Medicina General'),
    ]
    
    nombre = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad} {self.numero_documento}"