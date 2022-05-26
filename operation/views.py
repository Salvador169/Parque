import random

from django.contrib import messages
from django.utils import timezone
from django.shortcuts import render, redirect
from .forms import MatriculaForm, AssociarLugarForm
from .models import RegistoMovimento, Parque, Zona, Lugar, Viatura, Pagamento


# Create your views here.


def entrar_parque(request):
    return render(request=request,
                  template_name="main/entrar_parque.html",
                  context={"parques": Parque.objects.all()})


def entrar_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = MatriculaForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Entrou no parque com sucesso.")
            r = RegistoMovimento(data_de_entrada=timezone.now(), matricula=form.cleaned_data.get("matricula"),
                                 parqueid=parques)
            r.save()
            v = Viatura(registo_movimentoid=r, matricula=form.cleaned_data.get("matricula"))
            v.save()
            request.session['matricula'] = form.cleaned_data.get("matricula")
            return redirect("operation:index", parque_id=parque_id)
    else:
        form = MatriculaForm

    return render(request,
                  "main/entrar_parque_form.html",
                  context={"form": form, "parques": parques})


def index(request, parque_id):
    parque= Parque.objects.get(pk=parque_id)
    zonas = Zona.objects.filter(parqueid=parque)
    lugares = Lugar.objects.all()

    return render(request=request,
                  template_name="main/index.html",
                  context={"parque": parque, "zonas": zonas, "lugares": lugares})


def sair_parque_form(request, parque_id):
    parques = Parque.objects.get(pk=parque_id)
    if request.method == "POST":
        form = MatriculaForm(request.POST)
        if form.is_valid():
            v = Viatura.objects.filter(matricula=form.cleaned_data.get("matricula"))

            if RegistoMovimento.objects.filter(matricula=form.cleaned_data.get("matricula")).exists():
                r = RegistoMovimento(data_de_saida=timezone.now())
                r.save()
            else:
                messages.error(request, f"Matrícula não existe.")
                return redirect("operation:sair_parque_form")
            if v.exists():
                v.delete()
            else:
                messages.error(request, f"Matrícula não existe.")
                return redirect("operation:sair_parque_form")
            if not v.contratoid:
                p = Pagamento.objects.filter(viaturaid=v)
                if p.estado_do_pagamento is "Pendente":
                    messages.error(request, f"Tem um pagamento pendente.")
                    return redirect("operation:sair_parque_form")


        request.session.pop('matricula', None)
        request.session.modified = True
        messages.success(request, f"Saiu do parque com sucesso.")
        return redirect("operation:entrar_parque")

    else:
        form = MatriculaForm

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

    lugar = Lugar.objects.filter(pk=lugar_id)
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

    lugar = Lugar.objects.filter(pk=lugar_id)
    lugar.estado = "Livre"
    lugar.save()

    messages.success(request, f"Liberou o lugar no parque.")

    return redirect("operation:index", parque_id=parque_id)


def associar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(pk=zona_id)
    if request.method == "POST":
        form = AssociarLugarForm(request.POST)
        if form.is_valid():

            messages.success(request, f"Associou o lugar com sucesso.")

            zona.lugares = zona.lugares + 1
            zona.save()
            l = form.cleaned_data.get("lugar")
            l.zonaid = zona
            l.save()

            return redirect("operation:index", parque_id=parque_id)
    else:
        form = AssociarLugarForm

    return render(request,
                  "main/associar_lugar.html",
                  context={"form": form, "parques": parques})


def desassociar_lugar(request, parque_id, zona_id):
    parques = Parque.objects.get(pk=parque_id)
    zona = Zona.objects.get(pk=zona_id)
    if request.method == "POST":
        form = AssociarLugarForm(request.POST)
        if form.is_valid():
            messages.success(request, f"Associou o lugar com sucesso.")

            zona.lugares = zona.lugares - 1
            zona.save()
            l = form.cleaned_data.get("lugar")
            l.zonaid = None
            l.save()

            return redirect("operation:index", parque_id=parque_id)
    else:
        form = AssociarLugarForm

    return render(request,
                  "main/desassociar_lugar.html",
                  context={"form": form, "parques": parques})
