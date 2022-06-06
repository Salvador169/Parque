from multiprocessing import context
from django.shortcuts import get_object_or_404, render
from django.views import View

from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
    )

from .forms import ParqueModelForm, ZonaModelForm, LugarModelForm, ReclamacaoModelForm
from .models import Parque, Zona, Lugar, Reclamacao

def index_view(request, *args, **kwargs):
    return render(request, "home.html", {})


class ReclamacaoListView(View):
    template_name = 'reclamacao/reclamacao_list.html'
    queryset = Reclamacao.objects.all()

    def get(self, request, *args, **kwargs):
        context = {"object_list": self.queryset}
        return render(request, self.template_name, context)
        

class ReclamacaoCreateView(View):
    template_name = 'reclamacao/reclamacao_create.html'
    def get(self, request, *arg, **kwargs):
        form = ReclamacaoModelForm()
        context={"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *arg, **kwargs):
        form = ReclamacaoModelForm(request.POST)
        if form.is_valid():
            form.save()
            form = ReclamacaoModelForm()
        context={"form": form}
        return render(request, self.template_name, context)



#==================================================================================================
#Parque

class ParqueCreateView(CreateView):
    template_name = 'parque/parque_create.html'
    form_class = ParqueModelForm
    queryset = Parque.objects.all()

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return '../'



class ParqueListView(ListView):
    template_name = 'parque/parque_list.html'
    queryset = Parque.objects.all()



class ParqueDetailView(DetailView):
    template_name = 'parque/parque_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)



class ParqueUpdateView(UpdateView):
    template_name = 'parque/parque_create.html'
    form_class = ParqueModelForm
    queryset = Parque.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)

    def form_valid(self, form):
        return super().form_valid(form)



class ParqueDeleteView(DeleteView):
    template_name = 'parque/parque_delete.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Parque, id=id_)

    def get_success_url(self):
        return '../../../'



#==================================================================================================
#Zona

class ZonaListView(ListView):
    template_name = 'zona/zona_list.html'
    model = Zona

    def get_queryset(self):
        parque=Parque.objects.get(id=self.kwargs["id"])
        return Zona.objects.filter(parqueid=parque)



class ZonaDetailView(DetailView):
    template_name = 'zona/zona_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Zona, id=id_)



class ZonaCreateView(CreateView):
    template_name = 'zona/zona_create.html'
    form_class = ZonaModelForm
    model = Zona

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.parqueid = Parque.objects.get(id=self.kwargs["id"])
        return super(ZonaCreateView, self).form_valid(form)

    def get_success_url(self):
        return '../'



class ZonaUpdateView(UpdateView):
    template_name = 'zona/zona_create.html'
    form_class = ZonaModelForm
    model = Zona

    def form_valid(self, form):
        zona = form.save(commit=False)
        zona.parqueid = Parque.objects.get(id=self.kwargs["id"])
        return super(ZonaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return '../../'




class ZonaDeleteView(DeleteView):
    template_name = 'zona/zona_delete.html'
    model = Zona

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return '../../'



#==================================================================================================
#Lugar

class LugarListView(ListView):
    template_name = 'lugar/lugar_list.html'
    model = Lugar

    def get_queryset(self):
        zona=Zona.objects.get(id=self.kwargs["pk"])
        return Lugar.objects.filter(zonaid=zona)



class LugarDetailView(DetailView):
    template_name = 'lugar/lugar_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)



class LugarCreateView(CreateView):
    template_name = 'lugar/lugar_create.html'
    form_class = LugarModelForm
    model = Lugar

    def form_valid(self, form):
        lugar = form.save(commit=False)
        lugar.zonaid = Zona.objects.get(id=self.kwargs["pk"])
        return super(LugarCreateView, self).form_valid(form)

    def get_success_url(self):
        return '../'



class LugarUpdateView(UpdateView):
    template_name = 'lugar/lugar_create.html'
    form_class = LugarModelForm
    model = Lugar

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)

    def form_valid(self, form):
        lugar = form.save(commit=False)
        lugar.zonaid = Zona.objects.get(id=self.kwargs["pk"])
        return super(LugarUpdateView, self).form_valid(form)

    def get_success_url(self):
        return '../../'



class LugarDeleteView(DeleteView):
    template_name = 'lugar/lugar_delete.html'
    model = Lugar

    def get_object(self):
        id_ = self.kwargs.get("lugar")
        return get_object_or_404(Lugar, id=id_)

    def delete(self, *args, **kwargs):
        self.object = self.get_object()
        super().delete(*args, **kwargs)

    def get_success_url(self):
        return '../../'