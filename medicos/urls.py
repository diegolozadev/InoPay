from django.urls import path
from .views import MedicoCreateView, MedicoListView, MedicoDetailView, cargar_produccion_medico, ProduccionListView, exportar_produccion_excel, preparar_recibo, imprimir_recibo


urlpatterns = [
    path('medicos/', MedicoListView.as_view(), name='medico-list'),
    path('medicos/<int:pk>/', MedicoDetailView.as_view(), name='medico-detail'),
    path('medicos/nuevo/', MedicoCreateView.as_view(), name='medico-create'),
    path('medicos/<int:medico_id>/cargar-produccion/', cargar_produccion_medico, name='cargar-produccion-medico'),
    
    # 1. La pantalla para elegir fechas
    path('medico/<int:medico_id>/recibo/preparar/', preparar_recibo, name='preparar-recibo'),
    # 2. La pantalla limpia para imprimir
    path('medico/<int:medico_id>/recibo/imprimir/', imprimir_recibo, name='imprimir-recibo'),
    
    path('producciones/', ProduccionListView.as_view(), name='produccion-list'),
    path('producciones/exportar-excel/', exportar_produccion_excel, name='exportar-produccion-excel'),
    
]