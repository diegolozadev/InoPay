from django.contrib import admin
from .models import Tarifa

# Register your models here.

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio', 'unidad_negocio', 'fecha_registro', 'registrado_por')
    search_fields = ('nombre',)
    list_filter = ('precio',)
