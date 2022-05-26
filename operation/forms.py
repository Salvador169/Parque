from django import forms
from django.core.exceptions import ValidationError
import re
from .models import TabelaMatriculas, Zona, Lugar
from .models import RegistoMovimento, Viatura


class MatriculaForm(forms.Form):
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


class AssociarLugarForm(forms.Form):
    lugar = forms.ModelChoiceField(queryset=Lugar.objects.all(), widget=forms.Select)

    def clean_lugar(self):
        lugar = self.cleaned_data["lugar"]

        return lugar



