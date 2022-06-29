import django_tables2 as tables
from django_tables2.utils import A
from .models import Parque, Zona, Lugar

class ParqueTable(tables.Table):
    Ver_Mais = tables.LinkColumn('parque:parque-detail', text='Ver Mais', args=[A('id')])
    class Meta:
        model = Parque
        fields = ("nome", "capacidade", "zonas", "estado", "morada", "cidade", "codigo_postal" )

class ZonaTable(tables.Table):
    Ver_Mais = tables.TemplateColumn(template_name="table_zona.html")
    class Meta:
        model = Zona
        fields = ("numero_da_zona", "lugares", "tipo_da_zona")

class LugarTable(tables.Table):
    Ver_Mais = tables.TemplateColumn(template_name="table_lugar.html")
    class Meta:
        model = Lugar
        fields = ("numero_do_lugar", "estado")