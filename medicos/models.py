from django.db import models
from tarifas.models import Tarifa
from django.contrib.auth.models import User
from tarifas.models import Tarifa
# Create your models here.

# Modelo para representar a un médico
class Medico(models.Model):
    
    ESPECIALIDADES = [
        ('Neumología Adulto', 'Neumología Adulto'),
        ('Neumología Pediátrica', 'Neumología Pediátrica'),
        ('Alergología', 'Alergología'),
        ('Cardiología','Cardiología'),
        ('Internista', 'Internista'),
        ('Juntas Médicas', 'Juntas Médicas')
    ]
    
    SEDES = [
        ('Principal', 'Principal'),
        ('Cabecera', 'Cabecera'),
        ('Machado', 'Machado'),
        ('Prado', 'Prado'),
        ('Fosunab 6', 'Fosunab 6'),
        ('Fosunab 7', 'Fosunab 7'),
        ('Fosunab 8', 'Fosunab 8'),
    ]
    
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    nombre = models.CharField(max_length=100)
    numero_documento = models.CharField(max_length=20, unique=True)
    especialidad = models.CharField(max_length=100, choices=ESPECIALIDADES)
    email = models.EmailField(max_length=100, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    sede = models.CharField(max_length=100, choices=SEDES, default="Sin sede")
    
    # Relación de muchos a muchos
    servicios = models.ManyToManyField(Tarifa, related_name='medicos', blank=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Medico"
        verbose_name_plural = "Medicos"
    
    def __str__(self):
        return f"{self.nombre} - {self.especialidad} {self.numero_documento}"
    

# Modelo para representar la producción de un médico (servicios realizados)
class Produccion(models.Model):
    # Relaciones principales
    medico = models.ForeignKey(
        Medico, 
        on_delete=models.CASCADE, 
        related_name='producciones',
        verbose_name="Médico"
    )
    
    servicio = models.ForeignKey(
        Tarifa, 
        on_delete=models.PROTECT, # No permite borrar una tarifa si ya tiene producción ligada
        related_name='producciones_servicio',
        verbose_name="Servicio Realizado"
    )
    
    precio_aplicado = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False, # No editable porque se toma del servicio al momento de guardar
        verbose_name="Precio Aplicado"
    )
    
    # Guardan el texto exacto del momento
    sede_momento = models.CharField(max_length=100)
    unidad_negocio_momento = models.CharField(max_length=100)
    
    subunidad_momento = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name="Sub-Unidad al momento"
    )
    
    # Datos de la labor
    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name="Cantidad"
    )
    
    fecha_labor = models.DateField(
        verbose_name="Fecha de Realización"
    )
    
    # Auditoría (Trazabilidad)
    registrado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Persona Responsable"
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Sistema"
    )
    

    class Meta:
        verbose_name = "Registro de Producción"
        verbose_name_plural = "Registros de Producción"
        # Ordenar por lo más reciente por defecto
        ordering = ['-fecha_labor', '-fecha_registro']

    
    # Campo calculado cantidad * precio del servicio
    @property
    def subtotal(self):
        """Calcula el valor de esta línea de producción"""
        return self.cantidad * self.precio_aplicado
    
    def __str__(self):
        return f"{self.medico.nombre} - {self.servicio.nombre} ({self.cantidad})"