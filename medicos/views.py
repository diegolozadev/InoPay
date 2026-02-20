from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from medicos.forms import MedicoForm
from .models import Medico
from django.views.generic import ListView, DetailView, UpdateView, CreateView

# Create your views here.

# view para listar los médicos
class MedicoListView(ListView):
    model = Medico
    template_name = 'medicos/medico_list.html'
    context_object_name = 'medicos'

# view para mostrar el detalle de un médico y permitir su edición
class MedicoDetailView(UpdateView): # Cambiamos DetailView por UpdateView
    model = Medico
    form_class = MedicoForm # Importante: asignar formulario
    template_name = 'medicos/medico_detail.html'
    context_object_name = 'medico'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('medico-list')

# view para crear un nuevo médico
class MedicoCreateView(CreateView): # Cambiamos CreateView por UpdateView
    model = Medico
    form_class = MedicoForm # Importante: asignar formulario
    template_name = 'medicos/medico_create.html'
    context_object_name = 'medico'
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('medico-list')