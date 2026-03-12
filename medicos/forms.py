from medicos.models import Medico, Produccion
from django import forms

# formulario para crear o editar un médico
class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'numero_documento', 'especialidad', 'email', 'telefono', 'servicios', 'sede']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'servicios': forms.CheckboxSelectMultiple(),
            'sede': forms.Select(attrs={'class': 'form-control'})
        }

# formulario para crear o editar una producción (servicio realizado por un médico)
class ProduccionForm(forms.ModelForm):
    class Meta:
        model = Produccion
        # Solo necesitamos estos dos campos para la entrada masiva
        fields = ['fecha_labor', 'cantidad']
        widgets = {
            'fecha_labor': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'cantidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
        }

    # Validamos que la cantidad no sea negativa (por si acaso el HTML falla)
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 0:
            raise forms.ValidationError("La cantidad no puede ser negativa.")
        return cantidad