import django_tables2 as django_tables
from .models import Contrato
from django.utils.html import format_html
from django.urls import reverse


class ContratosTable(django_tables.Table):
    #Se aparecer um traco meter empty_values
    nome = django_tables.Column(accessor="nome", verbose_name="Nome", empty_values=())
    parque = django_tables.Column(accessor="parque", verbose_name="Parque", empty_values=())
    data_de_inicio = django_tables.Column('Data de Inicio')
    data_de_termino = django_tables.Column('Data de Termino')
    periodicidade = django_tables.Column('Periodicidade' ,empty_values=())
    # ver = django_tables.LinkColumn('contrato:contrato-detail', text='View', args=['record.id'])
    editar = django_tables.TemplateColumn(template_name='edit.html')
    apagar = django_tables.TemplateColumn(template_name='delete.html')
    validar = django_tables.TemplateColumn(template_name='validate.html')

    class Meta:
        model = Contrato
        # sequence = ('nome', 'email', 'contacto', 'tipo', 'valido', 'acoes')
        fields = ('nome', 'parque', 'data_de_inicio', 'data_de_termino', 'periodicidade')

    def render_nome(self, record):
        return record.clienteid.nome
    
    def render_parque(self, record):
        return record.parqueid.nome
    
    def render_periodicidade(self, record):
        return record.periodicidadeid.periodicidade