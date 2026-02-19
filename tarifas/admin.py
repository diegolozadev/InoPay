from django.contrib import admin
from .models import Servicio

# Register your models here.

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio')
    search_fields = ('nombre',)
    list_filter = ('precio',)
