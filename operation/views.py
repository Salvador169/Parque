import random

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView

from .forms import EntrarParqueForm, SairParqueForm, AssociarLugarForm, DesassociarLugarForm, ReclamacaoModelForm
from .models import RegistoMovimento, Parque, Zona, Lugar, Viatura, Pagamento, Reclamacao, Fatura


# Create your views here.

def entrar_parque(request):
    return render(request=request,
                  template_name="main/entrar_parque.html",
                  context={"parques": Parque.objects.all()})


def entrar_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = EntrarParqueForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Entrou no parque com sucesso.")
            r = RegistoMovimento(data_de_entrada=timezone.now(), matricula=form.cleaned_data.get("matricula"), parqueid=parques)
            r.save()
            v = Viatura(registo_movimentoid=r, matricula=form.cleaned_data.get("matricula"))
            v.save()

            return redirect("operation:index", parque_id=parque_id)
    else:
        form = EntrarParqueForm

    return render(request,
                  "main/entrar_parque_form.html",
                  context={"form": form, "parques": parques})


def index(request, parque_id):
    parque= Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.all()
    faturas = Fatura.objects.all()
    reclamacoes = Reclamacao.objects.all()

    return render(request=request,
                  template_name="main/index.html",
                  context={"parque": parque, "zonas": zonas, "lugares": lugares, "faturas": faturas, "reclamacoes": reclamacoes})


# Ver isto melhor
def sair_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = SairParqueForm(request.POST)
        if form.is_valid():
            v = Viatura.objects.filter(matricula=form.cleaned_data.get("matricula"))

            messages.success(request, f"Saiu do parque com sucesso.")
            return redirect("operation:entrar_parque")

    else:
        form = SairParqueForm

    return render(request,
                  "main/sair_parque_form.html",
                  context={"form": form, "parques": parques})


def ocupar_lugar(request, parque_id, lugar_id):
    parque = Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.none()
    for zona in zonas:
        lugares |= Lugar.objects.filter(zonaid=zona)

    lugares_livres = lugares.filter(estado="Livre")
    if not lugares_livres:
        messages.error(request, f"Não existem lugares livres no parque.")
        return redirect("operation:index", parque_id=parque_id)

    lugar = Lugar.objects.get(numero_do_lugar=lugar_id)
    lugar.estado = "Ocupado"
    lugar.save()

    messages.success(request, f"Ocupou o lugar no parque.")

    return redirect("operation:index", parque_id=parque_id)


def liberar_lugar(request, parque_id, lugar_id):
    parque = Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.none()
    for zona in zonas:
        lugares |= Lugar.objects.filter(zonaid=zona)

    lugares_ocupados = lugares.filter(estado="Ocupado")
    if not lugares_ocupados:
        messages.error(request, f"Não existem lugares ocupados no parque.")
        return redirect("operation:index", parque_id=parque_id)

    lugar = Lugar.objects.get(numero_do_lugar=lugar_id)
    lugar.estado = "Livre"
    lugar.save()

    messages.success(request, f"Liberou o lugar no parque.")

    return redirect("operation:index", parque_id=parque_id)


def associar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(numero_da_zona=zona_id)
    if request.method == "POST":
        form = AssociarLugarForm(zona, request.POST)
        if form.is_valid():

            messages.success(request, f"Associou o lugar com sucesso.")
            l = form.cleaned_data.get("lugar")
            m = form.cleaned_data.get("matricula")
            v = Viatura.objects.get(matricula=m)
            l.viaturaid = v
            l.save()

            return redirect("operation:index", parque_id=parque_id)
    else:
        form = AssociarLugarForm(zona)

    return render(request,
                  "main/associar_lugar.html",
                  context={"form": form, "parques": parques})


def desassociar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(numero_da_zona=zona_id)
    if request.method == "POST":
        form = DesassociarLugarForm(zona, request.POST)
        if form.is_valid():
            messages.success(request, f"Desassociou o lugar com sucesso.")

            l = form.cleaned_data.get("lugar")
            l.viaturaid = None
            l.save()

            return redirect("operation:index", parque_id=parque_id)
    else:
        form = DesassociarLugarForm(zona)

    return render(request,
                  "main/desassociar_lugar.html",
                  context={"form": form, "parques": parques})


def consultar_entradas(request, parque_id, fatura_id):
    parques = Parque.objects.get(pk=parque_id)
    fatura = Fatura.objects.get(id=fatura_id)
    p = fatura.pagamentoid
    v = p.viaturaid
    registos = RegistoMovimento.objects.filter(matricula=v.matricula)

    return render(request=request,
                  template_name="main/consultar_entradas.html",
                  context={"parques": parques, "fatura": fatura, "registos": registos})


def fazer_reclamacao(request, parque_id, fatura_id):
    parques = Parque.objects.get(pk=parque_id)
    fatura = Fatura.objects.get(id=fatura_id)

    if request.method == "POST":
        form = ReclamacaoModelForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Fez a reclamação com sucesso.")

            reclamacao = form.save(commit=False)
            reclamacao.faturaid = fatura
            reclamacao.save()

            return redirect("operation:consultar_entradas", parque_id=parque_id, fatura_id=fatura_id)
    else:
        form = ReclamacaoModelForm

    return render(request=request,
                  template_name="main/fazer_reclamacao.html",
                  context={"form": form, "parques": parques, "fatura": fatura})


def consultar_reclamacoes(request, parque_id, fatura_id):
    parques = Parque.objects.get(pk=parque_id)
    fatura = Fatura.objects.get(id=fatura_id)
    p = fatura.pagamentoid
    v = p.viaturaid
    registos = RegistoMovimento.objects.filter(matricula=v.matricula)

    return render(request=request,
                  template_name="main/consultar_entradas.html",
                  context={"parques": parques, "fatura": fatura, "registos": registos})

class ReclamacaoListView(View):
    template_name = 'reclamacao_list.html'
    queryset = Reclamacao.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)
