from django.db.models import Sum, F
from django.db.models.functions import TruncMonth
from django.utils import timezone
import json
# Importa tu modelo de producción
from medicos.models import Medico, Produccion
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Usamos 'fecha_labor' para agrupar y multiplicamos cantidad * precio_aplicado
        # Si la producción es (cantidad * precio), usamos ExpressionWrapper o F
        datos_raw = Produccion.objects.annotate(
            mes=TruncMonth('fecha_labor')
        ).values('mes').annotate(
            total=Sum(F('precio_aplicado') * F('cantidad')) 
        ).order_by('mes')[:6]

        # 2. Formatear para JS
        labels = [d['mes'].strftime('%b') if d['mes'] else "S/F" for d in datos_raw]
        valores = [float(d['total']) if d['total'] else 0 for d in datos_raw]

        context['labels_json'] = json.dumps(labels)
        context['valores_json'] = json.dumps(valores)
        
        # 3. Datos para las cards (Cálculo real de dinero)
        total_dinero = Produccion.objects.aggregate(
            total=Sum(F('precio_aplicado') * F('cantidad'))
        )['total'] or 0
        
        context['total_medicos'] = Medico.objects.count()
        context['produccion_total'] = total_dinero

        return context