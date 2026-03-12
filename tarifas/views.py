
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from .models import Tarifa
from tarifas.forms import TarifaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.db.models import Q

# Create your views here.

# view paara mostrar las tarifas
class TarifasView(LoginRequiredMixin, ListView):
    model = Tarifa
    template_name = 'tarifas/tarifas.html'
    context_object_name = 'tarifas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('id')
        q = self.request.GET.get('q')
        
        if q:
            # Filtra por nombre o descripción
            queryset = queryset.filter(
                Q(nombre__icontains=q) | 
                Q(descripcion__icontains=q) |
                Q(unidad_negocio__icontains=q)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['len_tarifas'] = Tarifa.objects.count() 
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
