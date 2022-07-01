from django.urls import path

from . import views

app_name = "operation"

urlpatterns = [
    path("", views.entrar_parque, name="entrar_parque"),
    path("entrar_parque_form/<int:parque_id>/", views.entrar_parque_form, name="entrar_parque_form"),
    path("index/<int:parque_id>/", views.index, name="index"),
    path("sair_parque_form/<int:parque_id>", views.sair_parque_form, name="sair_parque_form"),
    path("ocupar_lugar/<int:parque_id>/<int:lugar_id>/", views.ocupar_lugar, name="ocupar_lugar"),
    path("liberar_lugar/<int:parque_id>/<int:lugar_id>/", views.liberar_lugar, name="liberar_lugar"),
    path("associar_lugar/<int:parque_id>/<int:zona_id>/", views.associar_lugar, name="associar_lugar"),
    path("desassociar_lugar/<int:parque_id>/<int:zona_id>/", views.desassociar_lugar, name="desassociar_lugar"),

    # path('reclamacao/', views.ReclamacaoListView.as_view(), name='reclamacao-list'), #consultar reclamacoes
    # path("consultar_entradas/<int:parque_id>/<int:fatura_id>/", views.consultar_entradas, name="consultar_entradas"), #reclamar fatura
    path("reclamar_fatura/<int:parque_id>/<int:fatura_id>/", views.reclamar_fatura, name="reclamar_fatura"),
    path("processar_reclamacao/<int:parque_id>/<int:reclamacao_id>", views.processar_reclamacao, name="consultar_reclamacao"), #cancelar fatura
    # path('fatura/<int:id>/processar/', views.ProcessFaturaView.as_view(), name="processar_reclamacao"), #processar fatura
]