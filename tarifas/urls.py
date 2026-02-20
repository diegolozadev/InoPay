from django.urls import path
from .views import  TarifaCreateView, TarifasView, TarifaDetailView

urlpatterns = [
    path('tarifas/', TarifasView.as_view(), name='tarifas'),
    path('tarifas/<int:pk>/', TarifaDetailView.as_view(), name='tarifa_detail'),
    path('tarifas/nueva/', TarifaCreateView.as_view(), name='tarifa_create'),
]