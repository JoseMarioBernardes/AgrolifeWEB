from django.views.generic.edit import FormView
from django.db.models import Q
from django.shortcuts import render
from .models import Boi
from .forms import PeriodoForm

class RelatorioMortalidadeView(FormView):
    template_name = 'mortalidade/taxamortalidade.html'
    form_class = PeriodoForm

    def form_valid(self, form):
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']

        rebanho_inicial = Boi.objects.filter(
            data_entrada__lt=data_inicio
        ).filter(
            Q(data_saida__isnull=True) | Q(data_saida__gt=data_inicio),
            Q(data_morte__isnull=True) | Q(data_morte__gt=data_inicio)
        ).count()

        entradas = Boi.objects.filter(data_entrada__range=(data_inicio, data_fim)).count()
        mortes = Boi.objects.filter(data_morte__range=(data_inicio, data_fim)).count()

        rebanho_acumulado = rebanho_inicial + entradas
        taxa_mortalidade = (mortes / rebanho_acumulado) * 100 if rebanho_acumulado > 0 else 0

        contexto = self.get_context_data(form=form)
        contexto['resultado'] = {
            'rebanho_inicial': rebanho_inicial,
            'entradas': entradas,
            'rebanho_acumulado': rebanho_acumulado,
            'mortes': mortes,
            'taxa': round(taxa_mortalidade, 2),
        }
        return self.render_to_response(contexto)
