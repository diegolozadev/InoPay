from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from .models import Tarifa
from tarifas.forms import TarifaForm
from django.urls import reverse_lazy

# Create your views here.

# view paara mostrar las tarifas
class TarifasView(ListView):
    model = Tarifa
    template_name = 'tarifas/tarifas.html'
    context_object_name = 'tarifas'
    
# view para editar las tarifas
class TarifaDetailView(UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_detail.html'
    context_object_name = 'tarifa'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('tarifas')
    
# view para crear una nueva tarifa
class TarifaCreateView(CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_create.html'
    context_object_name = 'tarifa'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('tarifas')
