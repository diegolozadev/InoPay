from models import Medico
from django import forms

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = ['nombre', 'numero_documento', 'especialidad', 'email', 'telefono', 'fecha_registro']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_registro': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }