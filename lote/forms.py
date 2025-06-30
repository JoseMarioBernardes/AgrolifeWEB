from django import forms
from lote.models import Lote

class LoteModelForm(forms.ModelForm):

     class Meta:
        model = Lote
        fields = '__all__'
        widgets = {
            'data_inicio_lote': forms.DateInput(attrs={'type': 'date'})
        }