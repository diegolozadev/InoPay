from django import forms
from .models import Tarifa

class TarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['nombre', 'precio', 'descripcion', 'unidad_negocio', "subunidad_procedimientos"]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'unidad_negocio': forms.Select(attrs={'class': 'form-control'}),
            'subunidad_procedimientos': forms.Select(attrs={'class': 'form-control'}),
        }