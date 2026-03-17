
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView
from .models import Tarifa
from tarifas.forms import TarifaForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins  import LoginRequiredMixin
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

# view paara mostrar las tarifas
class TarifasView(LoginRequiredMixin, ListView):
    model = Tarifa
    template_name = 'tarifas/tarifas.html'
    context_object_name = 'tarifas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
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
class TarifaDetailView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_detail.html'
    context_object_name = 'tarifa'
    success_message = "¡Tarifa %(nombre)s actualizada con éxito!"
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('tarifas')
    
    # 1. HEREDAMOS DE PermissionRequiredMixin (arriba)
    # 2. DEFINIMOS EL PERMISO (app.permiso en minúsculas)
    permission_required = 'tarifas.change_tarifa'

    # 3. Si no tiene permiso, muestra el error 403 (Prohibido)
    raise_exception = True
    
# view para crear una nueva tarifa
class TarifaCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model = Tarifa
    form_class = TarifaForm
    template_name = 'tarifas/tarifa_create.html'
    success_message = "¡Tarifa %(nombre)s creada con éxito!"
    success_url = reverse_lazy('tarifas')
    
    # 1. HEREDAMOS DE PermissionRequiredMixin (arriba)
    # 2. DEFINIMOS EL PERMISO (app.permiso en minúsculas)
    permission_required = 'tarifas.add_tarifa'

    # 3. Si no tiene permiso, muestra el error 403 (Prohibido)
    raise_exception = True
    
    def form_valid(self, form):
        # Asignamos el usuario que está logueado a la columna registrado_por
        form.instance.registrado_por = self.request.user
        
        # Llamamos al método padre para que termine el guardado y el success_message
        return super().form_valid(form)
