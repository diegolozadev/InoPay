from django.contrib import admin
from .models import Tarifa

# Register your models here.

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio')
    search_fields = ('nombre',)
    list_filter = ('precio',)
