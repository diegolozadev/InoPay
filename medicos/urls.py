from django.urls import path
from .views import MedicoCreateView, MedicoListView, MedicoDetailView

urlpatterns = [
    path('medicos/', MedicoListView.as_view(), name='medico-list'),
    path('medicos/<int:pk>/', MedicoDetailView.as_view(), name='medico-detail'),
    path('medicos/nuevo/', MedicoCreateView.as_view(), name='medico-create'),
]