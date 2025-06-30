from django.urls import path
from relatorios.views import RelatorioMortalidadeView, RelatorioDoencasView, RelatorioAnimaisManejadosView, RelatorioMedicamentosPorProtocoloView

urlpatterns = [
    path('mortalidade/', RelatorioMortalidadeView.as_view(), name='relatorio_mortalidade'),
    path('doencas/', RelatorioDoencasView.as_view(), name='relatorio_doencas'),
    path('relatorios/manejos/', RelatorioAnimaisManejadosView.as_view(), name='relatorio_manejos'),
    path('relatorios/medicados-com-protocolo/', RelatorioMedicamentosPorProtocoloView.as_view(), name='relatorio_animais_medicados'),
    
]
