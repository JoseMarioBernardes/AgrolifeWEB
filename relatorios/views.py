from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.db.models import Q, F, Count, ExpressionWrapper, DecimalField
from boi.models import Boi
from relatorios.forms import PeriodoForm
from medicamento.models import AplicacaoEvento, MedicamentoAplicado
from manejo.models import Manejo, BoiManejo

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

class RelatorioDoencasView(FormView):
    template_name = 'doencas/relatorio_doencas.html'
    form_class = PeriodoForm

    def form_valid(self, form):
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']

        eventos = AplicacaoEvento.objects.filter(
            data_aplicacao_medicamento__range=(data_inicio, data_fim),
            doenca__isnull=False
        )

        total_animais = eventos.values('boi').distinct().count()

        doencas_agrupadas = eventos.values('doenca__nome_doenca') \
            .annotate(bois_tratados=Count('boi', distinct=True)) \
            .order_by('-bois_tratados')

        for d in doencas_agrupadas:
            d['percentual'] = round((d['bois_tratados'] / total_animais) * 100, 2) if total_animais > 0 else 0

        context = self.get_context_data(form=form)
        context['resultado'] = {
            'total_animais': total_animais,
            'doencas': doencas_agrupadas,
        }
        return self.render_to_response(context)
    
class RelatorioAnimaisManejadosView(FormView):
    template_name = 'manejo/relatorio_manejos.html'
    form_class = PeriodoForm

    def form_valid(self, form):
        data_inicio = form.cleaned_data['data_inicio']
        data_fim = form.cleaned_data['data_fim']

        manejos = Manejo.objects.filter(data_manejo__range=(data_inicio, data_fim)) \
            .select_related('tipo_manejo')

        dados_por_tipo = {}

        for tipo in manejos.values_list('tipo_manejo__nome_tipo_manejo', flat=True).distinct():
            manejos_tipo = manejos.filter(tipo_manejo__nome_tipo_manejo=tipo)
            
            contagem = (
                BoiManejo.objects
                .filter(manejo__in=manejos_tipo)
                .values('manejo__data_manejo')
                .annotate(total=Count('boi'))
                .order_by('manejo__data_manejo')
            )

            dados_por_tipo[tipo] = contagem

        context = self.get_context_data(form=form)
        context['resultado'] = dados_por_tipo
        return self.render_to_response(context)
    
class RelatorioMedicamentosPorProtocoloView(TemplateView):
    template_name = 'doencas/relatorio_medicamentos_protocolo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Seleciona bois que receberam protocolo
        bois_com_protocolo = BoiManejo.objects.filter(
            protocolo_sanitario__isnull=False
        ).values_list('boi_id', flat=True)

        # Medicamentos aplicados nesses bois
        aplicacoes = (
            MedicamentoAplicado.objects
            .filter(evento__boi_id__in=bois_com_protocolo)
            .select_related('medicamento', 'evento__boi')
            .annotate(
                preco_dose=ExpressionWrapper(
                    F('dose_aplicada') * F('medicamento__preco_ml'),
                    output_field=DecimalField(max_digits=8, decimal_places=2)
                )
            )
        )

        context['aplicacoes'] = aplicacoes
        return context