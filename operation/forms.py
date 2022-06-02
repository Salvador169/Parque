from django import forms
from django.core.exceptions import ValidationError
import re

from django.utils import timezone

from .models import TabelaMatriculas, Zona, Lugar, Pagamento
from .models import RegistoMovimento, Viatura


class EntrarParqueForm(forms.Form):
    matricula = forms.CharField(label=None)

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
    matricula = forms.CharField(label=None)

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]
        v = Viatura.objects.filter(matricula=matricula)

        if len(matricula) > 10:
            raise ValidationError("Matrícula deve conter menos de 11 caracteres.")

        if RegistoMovimento.objects.filter(matricula=matricula).exists():
            r = RegistoMovimento(data_de_saida=timezone.now())
            r.save()
        else:
            raise ValidationError("Matrícula não existe.")

        if v.exists():
            v.delete()
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
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar



