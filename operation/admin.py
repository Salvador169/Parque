from django.contrib import admin
from .models import Funcionario, Cliente, Viatura, Parque, RegistoMovimento, Contrato, Zona, Lugar, \
    Pagamento, TabelaMatriculas, Reserva, Fatura, Reclamacao

# Register your models here.


class ParqueAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Parque", {"fields": ["Nome", "Zonas"]}),
        ("Lugar", {"fields": ["Estado"]})
    ]


admin.site.register(TabelaMatriculas)
admin.site.register(Funcionario)
admin.site.register(Reserva)
admin.site.register(Parque)
admin.site.register(Zona)
admin.site.register(Lugar)
admin.site.register(RegistoMovimento)
admin.site.register(Cliente)
admin.site.register(Viatura)
admin.site.register(Contrato)
admin.site.register(Pagamento)
admin.site.register(Fatura)
admin.site.register(Reclamacao)

