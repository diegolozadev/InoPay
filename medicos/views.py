from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from medicos.forms import MedicoForm
from .models import Medico, Produccion, Tarifa
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count # Importante para buscar por varios campos
import openpyxl

# Create your views here.

# view para listar los médicos
class MedicoListView(LoginRequiredMixin, ListView):
    model = Medico
    template_name = 'medicos/medico_list.html'
    context_object_name = 'medicos'
    paginate_by = 12
    
    
    def get_queryset(self):
        # Usamos prefetch_related para traer los servicios de un solo golpe
        queryset = Medico.objects.prefetch_related('servicios')
        
        # Lógica de búsqueda por medicos
        q = self.request.GET.get('q')
        if q:
                    queryset = queryset.filter(
                        Q(nombre__icontains=q) | 
                        Q(numero_documento__icontains=q)
                    )
                
        return queryset.order_by('nombre')

# view para mostrar el detalle de un médico y permitir su edición
class MedicoDetailView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Medico
    form_class = MedicoForm # Importante: asignar formulario
    template_name = 'medicos/medico_detail.html'
    context_object_name = 'medico'
    success_message = "¡Médico %(nombre)s actualizado con éxito!"

    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('medico-list')

# view para crear un nuevo médico
class MedicoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Medico
    form_class = MedicoForm # Importante: asignar formulario
    template_name = 'medicos/medico_create.html'
    context_object_name = 'medico'
    success_message = "¡Médico %(nombre)s creado con éxito!"
    
    # A dónde redirigir tras guardar con éxito
    success_url = reverse_lazy('medico-list')
    
    def form_valid(self, form):
        # El objeto 'form.instance' es el médico que se está creando
        # Le asignamos el usuario que está navegando (self.request.user)
        form.instance.registrado_por = self.request.user
        
        # Luego llamamos al método original para que guarde todo
        return super().form_valid(form)
    

# view para cargar producciones (servicios realizados por un médico) de forma masiva
@login_required
def cargar_produccion_medico(request, medico_id):
    """
    Registra de forma masiva la producción mensual de un médico.
    Captura el precio actual de la tarifa y lo guarda permanentemente
    en cada registro para evitar cambios históricos.
    """
    # 1. Obtener datos iniciales
    medico = get_object_or_404(Medico, pk=medico_id)
    # Traemos los servicios del médico para el formulario
    servicios = medico.servicios.all()
    hoy = timezone.now().date()

    if request.method == 'POST':
        fecha_labor = request.POST.get('fecha_labor')
        # Obtenemos las listas enviadas desde los múltiples inputs del HTML
        servicios_ids = request.POST.getlist('servicio_id')
        cantidades = request.POST.getlist('cantidad')

        # OPTIMIZACIÓN: Traemos todos los objetos de Tarifa de una vez
        # Así evitamos hacer una consulta a la DB por cada fila de la tabla
        tarifas_dict = {str(t.id): t for t in Tarifa.objects.filter(id__in=servicios_ids)}
        
        registros_a_crear = []

        # 2. Procesar las entradas del formulario
        for servicio_id, cant in zip(servicios_ids, cantidades):
            try:
                # Validamos que la cantidad sea un número entero y positivo
                valor = int(cant) if cant and int(cant) > 0 else 0
            except ValueError:
                valor = 0
            
            if valor > 0:
                # Obtenemos el objeto tarifa desde nuestro diccionario en memoria
                servicio_obj = tarifas_dict.get(servicio_id)
                
                if servicio_obj:
                    # Creamos la instancia en memoria (sin guardar aún)
                    registros_a_crear.append(
                        Produccion(
                            medico=medico,
                            servicio=servicio_obj,
                            cantidad=valor,
                            fecha_labor=fecha_labor,
                            registrado_por=request.user,
                            # PUNTO CLAVE: "Congelamos" el precio actual aquí
                            precio_aplicado=servicio_obj.precio, # Esto protege el histórico si la tarifa sube después
                            sede_momento=medico.sede, # Viene del modelo Medico
                            unidad_negocio_momento=servicio_obj.unidad_negocio # Viene de Tarifa
                        )
                    )

        # 3. Validaciones de negocio
        if not registros_a_crear:
            messages.error(request, "¡Atención! No se ingresó ninguna cantidad válida. Intente de nuevo.")
            return render(request, 'medicos/cargar_produccion.html', {
                'medico': medico,
                'servicios': servicios,
                'hoy': hoy,
                'fecha_seleccionada': fecha_labor, # Mantenemos la fecha para comodidad del usuario
            })

        # 4. Carga masiva
        try:
            # bulk_create inserta todos los registros en una sola sentencia SQL
            Produccion.objects.bulk_create(registros_a_crear)
            messages.success(request, f"Se registraron {len(registros_a_crear)} servicios para el Dr. {medico.nombre} con éxito.")
            return redirect('medico-list')
        except Exception as e:
            # Manejo de errores por si algo falla en la base de datos
            messages.error(request, f"Hubo un error al guardar: {str(e)}")

    # Respuesta para método GET
    return render(request, 'medicos/cargar_produccion.html', {
        'medico': medico,
        'servicios': servicios,
        'hoy': hoy
    })

# view para listar las producciones de todos los médicos
class ProduccionListView(LoginRequiredMixin, ListView):
    model = Produccion
    template_name = 'medicos/produccion_list.html'
    context_object_name = 'producciones'
    paginate_by = 15 
    
    def get_queryset(self):
        # Mantenemos la lógica de filtrado para la tabla
        queryset = super().get_queryset().select_related('medico', 'servicio')
        
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        medico_id = self.request.GET.get('medico')

        if fecha_inicio and fecha_fin:
            queryset = queryset.filter(fecha_labor__range=[fecha_inicio, fecha_fin])
        
        if medico_id:
            queryset = queryset.filter(medico_id=medico_id)
            
        return queryset.order_by('-fecha_labor', '-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # TOTAL GLOBAL: Este contador ignora los filtros del queryset
        # Muestra absolutamente todo lo que hay en la tabla Produccion
        context['total_general'] = Produccion.objects.count()
        
        context['medicos'] = Medico.objects.all()
        return context


@login_required
def exportar_produccion_excel(request):
    # 1. Capturamos los filtros que vienen en la URL (?fecha_inicio=...&medico=...)
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    medico_id = request.GET.get('medico')

    # 2. Aplicamos los filtros al queryset
    queryset = Produccion.objects.all().select_related('medico', 'servicio')
    
    if fecha_inicio and fecha_fin:
        queryset = queryset.filter(fecha_labor__range=[fecha_inicio, fecha_fin])
    if medico_id:
        queryset = queryset.filter(medico_id=medico_id)

    # 3. Creamos el libro de Excel en memoria
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Consolidado Producción"

    # Definimos los encabezados (incluyendo Unidad de Negocio)
    headers = ['Fecha', 'Médico', 'U. Negocio', 'Servicio', 'Cantidad', 'Precio Aplicado', 'Subtotal']
    ws.append(headers)

    # 4. Llenamos las filas con la producción
    total_general = 0
    for p in queryset:
        subtotal = p.cantidad * p.precio_aplicado
        total_general += subtotal
        ws.append([
            p.fecha_labor.strftime('%d/%m/%Y') if hasattr(p.fecha_labor, 'strftime') else str(p.fecha_labor),
            p.medico.nombre,
            p.servicio.unidad_negocio,
            p.servicio.nombre,
            p.cantidad,
            p.precio_aplicado,
            subtotal
        ])

    # Fila final de Total
    ws.append(['', '', '', '', '', 'TOTAL GENERAL:', total_general])

    # 5. Configuramos la respuesta del navegador para que descargue el archivo
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="Reporte_Produccion.xlsx"'
    
    # Guardamos el libro en la respuesta
    wb.save(response)
    return response


# view para preparar el recibo (pantalla de selección de fechas y resumen) y luego imprimirlo (pantalla limpia para impresión)
@login_required
def preparar_recibo(request, medico_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    
    # Intentamos obtener fechas si el usuario ya filtró
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    producciones = None
    total = 0

    if fecha_inicio and fecha_fin:
        # Buscamos la producción en ese rango
        producciones = Produccion.objects.filter(
            medico=medico,
            fecha_labor__range=[fecha_inicio, fecha_fin]
        ).select_related('servicio')
        
        # Calculamos el total sumando los subtotales de cada registro
        total = sum(p.subtotal for p in producciones)

    return render(request, 'medicos/preparar_recibo.html', {
        'medico': medico,
        'producciones': producciones,
        'total': total,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

# view para mostrar el recibo en formato limpio para impresión
@login_required
def imprimir_recibo(request, medico_id):
    medico = get_object_or_404(Medico, pk=medico_id)
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    producciones = Produccion.objects.filter(
        medico=medico,
        fecha_labor__range=[fecha_inicio, fecha_fin]
    ).select_related('servicio')
    
    total = sum(p.subtotal for p in producciones)

    return render(request, 'medicos/recibo_impresion_final.html', {
        'medico': medico,
        'producciones': producciones,
        'total': total,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'hoy': timezone.now()
    })