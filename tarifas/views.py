from django.shortcuts import render
from django.views.generic import ListView
from .models import Tarifa

# Create your views here.

# view paara mostrar las tarifas
class TarifasView(ListView):
    model = Tarifa
    template_name = 'tarifas/tarifas.html'
    context_object_name = 'tarifas'
