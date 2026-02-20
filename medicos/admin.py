# medicos/admin.py
from django.contrib import admin
from .models import Medico, Produccion

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    # Columnas que verás en la lista principal
    list_display = ('nombre', 'numero_documento', 'especialidad', 'email', 'telefono','fecha_registro', 'registrado_por')
    
    # Buscador para no estar bajando por toda la lista
    search_fields = ('nombre', 'numero_documento')
    
    # Filtro lateral por especialidad
    list_filter = ('especialidad',)
    
    # PARA MOSTRAR LOS SERVICIOS:
    # Esto crea la interfaz de dos columnas para los ManyToMany
    filter_horizontal = ('servicios',)

@admin.register(Produccion)
class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('medico', 'servicio', 'cantidad', 'subtotal', 'fecha_registro')
    list_filter = ('medico', 'fecha_registro')