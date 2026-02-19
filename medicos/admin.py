from django.contrib import admin
from .models import Medico

# Register your models here.

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_documento', 'especialidad', 'email', 'telefono', 'fecha_registro')
    search_fields = ('nombre', 'especialidad', 'numero_documento')
    list_filter = ('especialidad', 'fecha_registro')