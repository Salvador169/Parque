import datetime
from django.urls import reverse
import stripe
import json
from django.core.mail import send_mail
from django.conf import settings
from multiprocessing import context
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import MultiTableMixin, SingleTableMixin, SingleTableView
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage

from PaymentManagement import urls
from .models import Cliente, Contrato, Dia, Fatura, Lugar, Pagamento, Parque, Periodicidade, Reclamacao, RegistoMovimento, Reserva, TabelaPrecos
from .forms import ContratoForm, FaturaModelForm, PaymentModelForm, PaymentProveModelForm, ReclamacaoModelForm
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView, 
    TemplateView, 
    View
    )

from .tables import ContratosTable
from django_filters.views import FilterView
from .filters import ContratosFilter
from django.db.models import F
from django.template import loader

stripe.api_key = settings.STRIPE_SECRET_KEY

#LISTAR OS CONTRATOS
class contratos_list(SingleTableMixin, FilterView):
    table_class = ContratosTable
    template_name = 'contratos.html'
    filterset_class = ContratosFilter
    table_pagination = {
        'per_page': 10
    }

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(SingleTableMixin, self).get_context_data(**kwargs)
        table = self.get_table(**self.get_table_kwargs())
        context[self.get_context_table_name(table)] = table
        return context
    
#CONSULTAR CONTRATO
def contrato_detail_view(request, id):
    contrato=Contrato.objects.get(id=id)
    lugar=Lugar.objects.get(contratoid=contrato)
    dias=Dia.objects.filter(periodicidadeid=contrato.periodicidadeid)
    template = loader.get_template('detail.html')
    context ={
        'contrato': contrato,
        'lugar':lugar,
        'dias':dias,
    }
    return HttpResponse(template.render(context, request))

#APAGAR CONTRATO
def contrato_delete_view(request, id):
    contrato=Contrato.objects.get(id=id)
    lugar = Lugar.objects.get(contratoid=contrato)
    if request.POST:
        contrato.delete()
        oldLugar = lugar
        oldLugar.contratoid=None
        oldLugar.save()
        return redirect('../../')
    template = loader.get_template('delete_confirmation.html')
    context ={
        "contrato": contrato,
    }
    return HttpResponse(template.render(context, request))

#LISTAR PARQUES
def contrato_parque_view(request):
    parques = Parque.objects.all()
    template = loader.get_template('parque.html')
    context ={
        'parques': parques,
    }
    return HttpResponse(template.render(context, request))

#CRIAR CONTRATO
def contrato_create_view(request, id):
    if request.method=='POST':
        form = ContratoForm(request.POST, current_user=Cliente.objects.get(id=1), parque=Parque.objects.get(id=id))
        if form.is_valid():
            form.save()
            contrato = Contrato.objects.latest("id")
            return redirect(reverse('PaymentManagement:contrato-pay', kwargs={ 'id': contrato.id }))
    else:
        form = ContratoForm(current_user=Cliente.objects.get(id=1))
    context ={
        'form': form,
    }
    return render(request, "create.html", context)

#EDITAR CONTRATO
def contrato_update_view(request, id):
    obj=get_object_or_404(Contrato, id=id)
    form = ContratoForm(request.POST or None, current_user=Cliente.objects.get(id=1), instance=obj)
    if form.is_valid():
        form.save(id)
        contrato = Contrato.objects.latest("id")
        return redirect(reverse('PaymentManagement:contrato-pay', kwargs={ 'id': contrato.id }))
    context ={
        'form': form,
    }
    return render(request, "create.html", context)


#APROVAR CONTRATO
def contrato_validate_aprove_view(request, id):
    contrato=Contrato.objects.get(id=id)
    contrato.valido = True
    contrato.save()
    return redirect('../../..')

#DESAPROVAR CONTRATO
def contrato_validate_desaprove_view(request, id):
    contrato=Contrato.objects.get(id=id)
    contrato.valido = False
    contrato.save()
    return redirect('../../..')


#CONSULTAR PAGAMENTOS
class payment_view(ListView):
    template_name = 'pagamentos.html'
    queryset = Pagamento.objects.all()
    faturas = Fatura.objects.values_list("pagamentoid", flat=True)

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset, "faturas": self.faturas}
        return render(request, self.template_name, context)

#PAGAMENTO EFETUADO COM SUCESSO
class SuccessView(TemplateView):
    template_name = "success.html"


#PAGAMENTO CANCELADO
class CancelView(TemplateView):
    template_name = "cancel.html"

class FaturaListView(View):
    template_name = 'fatura_list.html'
    queryset = Fatura.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)

class FaturaDeleteView(DeleteView):
    template_name = 'fatura_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Fatura, id=id_)

    def get_success_url(self):
        return '../../'

class ReclamacaoListView(View):
    template_name = 'reclamacao_list.html'
    queryset = Reclamacao.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)

class ReclamacaoCreateView(CreateView):
    template_name = 'reclamacao_create.html'
    form_class = ReclamacaoModelForm
    model = Reclamacao

    def form_valid(self, form):
        reclamacao = form.save(commit=False)
        reclamacao.faturaid = Fatura.objects.get(id=self.kwargs["id"])
        reclamacao.save()
        return redirect("../../")

    def get_success_url(self):
        return '../'

def payment_prove_create_view(request, id):
    if request.method == "POST":
        pagamento = Pagamento.objects.get(id=id)
        # if the post request has a file under the input name 'document', then save the file.
        request_file = request.FILES['document'] if 'document' in request.FILES else None
        if request_file:
                # save attached file
    
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                pagamento.comprovativo = request_file
                pagamento.save()
    
    return render(request, "payment_prove.html")

def payment_create_view(request, id):
    if request.method=='POST':
        form = PaymentModelForm(request.POST)
        contrato = Contrato.objects.get(id = id)
        payment = Pagamento.objects.get(contratoid=contrato)
        if form.is_valid():
            payment.estado_do_pagamento = "Pago"
            payment.save()
            return redirect('../')
    else:
        form = PaymentModelForm()
        contrato = Contrato.objects.get(id = id)

    price = TabelaPrecos.getPrice(contrato = contrato, all=False)
    context ={
        'form': form,
        'price': price,
    }
    return render(request, "payment.html", context)

def reserva_payment_create_view(request, id):
    reserva = Reserva.objects.get(id = id)
    price = TabelaPrecos.getPrice(reserva = reserva, date=reserva.data_de_inicio, all=False)
    if request.method=='POST':
        form = PaymentModelForm(request.POST)   
        if form.is_valid():
            payment = Pagamento()
            payment.data_de_vencimento = datetime.datetime.now()
            payment.estado_do_pagamento = "Pago"
            payment.montante = price
            payment.reservaid = reserva
            payment.save()
            return redirect('../../../')
    else:
        form = PaymentModelForm()

    
    context ={
        'form': form,
        'price': price,
    }
    return render(request, "payment.html", context)

def registo_payment_create_view(request, id):
    registo = RegistoMovimento.objects.get(id = id)
    price = TabelaPrecos.getPrice(registo = registo, all=False)
    if request.method=='POST':
        form = PaymentModelForm(request.POST)
        if form.is_valid():
            payment = Pagamento()
            payment.data_de_vencimento = datetime.datetime.now()
            payment.estado_do_pagamento = "Pago"
            payment.montante = price
            payment.registoid = registo
            payment.save()
            return redirect('../../../')
    else:
        form = PaymentModelForm()

    
    context ={
        'form': form,
        'price': price,
    }
    return render(request, "payment.html", context)

class OptionsView(TemplateView):
    template_name = "options.html"


def emit_fatura_view(request, id):
    payment=Pagamento.objects.get(id=id)
    newFatura = Fatura()
    newFatura.nomeEmpresa = "Parques Lda."
    newFatura.moradaEmpresa = "Faro"
    newFatura.nifEmpresa = 987654321
    newFatura.clienteid = Cliente.objects.get(id=1)
    newFatura.pagamentoid = payment
    newFatura.save()
    return redirect('../../')

class ProcessFaturaView(UpdateView):
    template_name = 'fatura_create.html'
    form_class = FaturaModelForm
    queryset = Fatura.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Fatura, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '../../'