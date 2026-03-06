
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from .models import Tarifa
from tarifas.forms import TarifaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins  import LoginRequiredMixin

# Create your views here.

# view paara mostrar las tarifas
class TarifasView(LoginRequiredMixin, ListView):
    model = Tarifa
    template_name = 'tarifas/tarifas.html'
    context_object_name = 'tarifas'
    paginate_by = 10 # Opcional: para paginar resultados
    len_tarifas = Tarifa.objects.count() # Contar el total de tarifas para mostrar en la plantilla
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_tarifas'] = self.len_tarifas # Agregar el conteo al contexto
        return context
    
# view para editar las tarifas
class TarifaDetailView(LoginRequiredMixin, UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_detail.html'
    context_object_name = 'tarifa'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('tarifas')
    
# view para crear una nueva tarifa
class TarifaCreateView(LoginRequiredMixin, CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_create.html'
    context_object_name = 'tarifa'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('tarifas')
