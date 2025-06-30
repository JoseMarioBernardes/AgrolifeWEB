from django import forms
from boi.models import Boi, StatusBoi

class BoiModelForm(forms.ModelForm):
    class Meta:
        model = Boi
        fields = [
            "brinco",
            "chip",
            "fornecedor",
            "raca",
            "sexo",
            "peso_entrada",
            "data_nascimento",
            "data_entrada",
            "lote",
        ]
        widgets = {
            "data_nascimento": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "data_entrada":    forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "brinco":          forms.TextInput(attrs={"class": "form-control"}),
            "chip":            forms.TextInput(attrs={"class": "form-control"}),
            "peso_entrada":    forms.NumberInput(attrs={"class": "form-control"}),
            "fornecedor":      forms.Select(attrs={"class": "form-control"}),
            "raca":            forms.Select(attrs={"class": "form-control"}),
            "sexo":            forms.Select(attrs={"class": "form-control"}),
            "lote":            forms.Select(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        status_ativo = StatusBoi.objects.get(nome_status='Ativo')
        self.instance.status_boi = status_ativo
        return super().save(commit=commit)

class BoiMorteForm(forms.ModelForm):
    class Meta:
        model = Boi

        fields = ["data_morte", "motivo_morte", "necropsia"]
        labels = {
            "data_morte":   "Data da Morte",
            "motivo_morte": "Motivo da Morte",
            "necropsia":    "Necropsia Realizada?",
        }
        widgets = {
            "data_morte":   forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "motivo_morte": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "necropsia":    forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['data_morte'].required = True
        self.fields['motivo_morte'].required = True

    def save(self, commit=True):
        status_morto = StatusBoi.objects.get(nome_status='Morto')
        self.instance.status_boi = status_morto

        return super().save(commit=commit)