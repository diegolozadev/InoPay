from django.urls import path
from .views import TarifasView

urlpatterns = [
    path('tarifas/', TarifasView.as_view(), name='tarifas'),
]