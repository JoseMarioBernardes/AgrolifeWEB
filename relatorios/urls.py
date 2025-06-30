from django.urls import path
from .views import RelatorioMortalidadeView

urlpatterns = [
    path('mortalidade/', RelatorioMortalidadeView.as_view(), name='relatorio_mortalidade'),
    path('relatorios/doencas/', RelatorioDoencasView.as_view(), name='relatorio_doencas'),
]
