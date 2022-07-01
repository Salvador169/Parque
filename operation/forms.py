from django import forms
from django.core.exceptions import ValidationError
import re

from django.utils import timezone

from .models import TabelaMatriculas, Lugar
from .models import RegistoMovimento, Viatura


class EntrarParqueForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]
        v = Viatura.objects.filter(matricula=matricula)

        if v.exists():
            raise ValidationError("Matrícula já existe no parque.")

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')
        for formato in t:
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)
            if pattern.match(matricula) is not None:
                break
            else:
                raise ValidationError("Matrícula com formato incorreto.")

        return matricula


class SairParqueForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        if RegistoMovimento.objects.filter(matricula=matricula).exists():
            r = RegistoMovimento(matricula=matricula, data_de_saida=timezone.now())
            r.save()
        else:
            raise ValidationError("Matrícula não existe.")

        # p = Pagamento.objects.filter(viaturaid=v)
        #
        # if p.exists():
        #     if p.estado_do_pagamento == "Pendente":
        #         if not v.contratoid:
        #             raise ValidationError("Tem um pagamento pendente.")

        t = TabelaMatriculas.objects.values_list('formato')
        for formato in t:
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)
            if pattern.match(matricula) is not None:
                break
            else:
                raise ValidationError("Matrícula com formato incorreto.")

        return matricula


class AssociarLugarForm(forms.Form):
    matricula = forms.CharField(label="Matrícula")
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def __init__(self, zona, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(zonaid=zona, estado="Livre")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')
        for formato in t:
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)
            if pattern.match(matricula) is not None:
                break
            else:
                raise ValidationError("Matrícula com formato incorreto.")

        return matricula

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar


class DesassociarLugarForm(forms.Form):
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def __init__(self, zona, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["lugar"].queryset = Lugar.objects.filter(zonaid=zona, estado="Ocupado")

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')
        for formato in t:
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)
            if pattern.match(matricula) is not None:
                break
            else:
                raise ValidationError("Matrícula com formato incorreto.")

        return matricula

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar


class ReclamacaoForm(forms.Form):
    reclamacao = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'size': '100', 'placeholder':'Escreva aqui a sua reclamação'}),
        required=True
        )
    registo = forms.ModelChoiceField(queryset=RegistoMovimento.objects.all(), widget=forms.Select)

    def __init__(self, fatura, *args, **kwargs):
        super().__init__(*args, **kwargs)
        p = fatura.pagamentoid
        v = p.viaturaid
        self.fields["registo"].queryset = RegistoMovimento.objects.filter(matricula=v.matricula)

    def clean_reclamacao(self):
        reclamacao = self.cleaned_data["reclamacao"]

        return reclamacao

    def clean_registo(self):
        registo = self.cleaned_data["registo"]

        return registo


class RegistoMovimentoModelForm(forms.ModelForm):
    matricula = forms.CharField(max_length=120, required=True)
    data_de_entrada = forms.DateTimeField(required=True)
    data_de_saida = forms.DateTimeField(required=False)
    provas = forms.CharField(max_length=120, required=False)

    def __init__(self, registo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["matricula"].initial = registo.matricula
        self.fields["data_de_entrada"].initial = registo.data_de_entrada
        self.fields["data_de_saida"].initial = registo.data_de_saida
        self.fields["provas"].initial = registo.provas


    class Meta:
        model = RegistoMovimento
        fields = [
            'matricula',
            'data_de_entrada',
            'data_de_saida',
            'provas']

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        t = TabelaMatriculas.objects.values_list('formato')
        for formato in t:
            formato = str(formato)
            formato = formato.replace("'", "")
            formato = formato.replace(",", "")
            formato = formato.replace("(", "")
            formato = formato.replace(")", "")
            pattern = re.compile(formato)
            if pattern.match(matricula) is not None:
                break
            else:
                raise ValidationError("Matrícula com formato incorreto.")

        return matricula

    def clean_data_de_entrada(self):
        data_de_entrada = self.cleaned_data["data_de_entrada"]

        return data_de_entrada

    def clean_data_de_saida(self):
        data_de_saida = self.cleaned_data["data_de_saida"]
        data_de_entrada = self.cleaned_data["data_de_entrada"]

        if data_de_saida < data_de_entrada:
            raise ValidationError("Data de saída é inferior à data de entrada.")

        return data_de_saida

    def clean_provas(self):
        provas = self.cleaned_data["provas"]

        return provas