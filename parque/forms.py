from secrets import choice
from django import forms
from .models import Parque, Zona, Lugar, Reclamacao

class ParqueModelForm(forms.ModelForm):
    nome = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={'placeholder':'Enter the name of the park','rows':1,'cols':20}),
        required=True
        )
    capacidade = forms.IntegerField(
        min_value=100,
        initial=100,
        required=True
        )
    zonas = forms.IntegerField(
        min_value=1,
        initial=1,
        required=True
        )
    estado = forms.ChoiceField(
        choices=Parque.make_options(),
        required=True
        )
    morada = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder':'Enter the address of the park','rows':1,'cols':120}),
        required=True
        )
    codigo_postal = forms.IntegerField(
        required=True
        )
    cidade = forms.CharField(
        required=True
        )

    class Meta:
        model = Parque
        fields = [
            'nome',
            'capacidade',
            'zonas',
            'estado',
            'morada',
            'cidade',
            'codigo_postal',
        ]

    def clean_morada(self, *args, **kwargs):
        morada = self.cleaned_data.get("morada")

        if ("Rua" in morada):
            return morada
        elif ("rua" in morada):
            return morada
        elif ("Avenida" in morada):
            return morada
        elif ("avenida" in morada):
            return morada
        elif ("estrada" in morada):
            return morada
        elif ("Estrada" in morada):
            return morada
        elif ("mansão" in morada):
            return morada
        elif ("Mansão" in morada):
            return morada
        elif ("urbanização" in morada):
            return morada
        elif ("Urbanização" in morada):
            return morada
        else:
            raise forms.ValidationError("A morada é inválida.")

    def clean_cidade(self, *args, **kwargs):
        cidade = self.cleaned_data.get("cidade")
        print(cidade)

        if((cidade == "Aveiro","Beja","Braga","Bragança","Castelo Branco","Coimbra","Évora","Faro","Guarda","Leiria","Lisboa","Portalegre","Porto","Santarém","Setúbal","Viana do Castelo","Vila Real","Viseu")):
            return cidade
        else:
           raise forms.ValidationError("Insira um dos 16 distritos de Portugal Continental.")

    def clean_codigo_postal(self, *args, **kwargs):
        cidade = self.cleaned_data.get("cidade")
        codigo_postal = self.cleaned_data.get("codigo_postal")

        if ((cidade=="Aveiro") and (codigo_postal != 3800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Aveiro. Quereria dizer 3800?")
        
        elif ((cidade=="Beja") and (codigo_postal != 7800)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Beja. Quereria dizer 7800?")
        
        elif ((cidade=="Braga") and (codigo_postal != 4700)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Braga. Quereria dizer 4700?")
        
        elif ((cidade=="Bragança") and (codigo_postal != 5300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Bragança. Quereria dizer 5300?")

        elif ((cidade=="Castelo Branco") and (codigo_postal != 6000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Castelo Branco. Quereria dizer 6000?")
        
        elif ((cidade=="Coimbra") and (codigo_postal != 3000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Coimbra. Quereria dizer 3000?")
        
        elif ((cidade=="Évora") and (codigo_postal != 7000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Évora. Quereria dizer 7000?")
        
        elif ((cidade=="Faro") and (codigo_postal != 8000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Faro. Quereria dizer 8000?")

        elif ((cidade=="Guarda") and (codigo_postal != 6300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Guarda. Quereria dizer 6300?")

        elif ((cidade=="Leiria") and (codigo_postal != 2400)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Leiria. Quereria dizer 2400?")

        elif ((cidade=="Lisboa") and (codigo_postal<1000 or codigo_postal>1900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Lisboa. Quereria dizer 1000 a 1900?")

        # elif ((cidade=="Funchal") and (codigo_postal != 9000)):
        #     raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Funchal. Quereria dizer 9000?")

        elif ((cidade=="Portalegre") and (codigo_postal != 7300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Portalegre. Quereria dizer 7300?")

        # elif ((cidade=="Ponta Delgada") and (codigo_postal != 9500)):
        #     raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Ponta Delgada. Quereria dizer 9500?")

        elif ((cidade=="Porto") and (codigo_postal<4000 or codigo_postal>4300)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade do Porto. Quereria dizer 4000 a 4300?")

        elif ((cidade=="Santarém") and (codigo_postal != 2000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Santarém. Quereria dizer 2000?")

        elif ((cidade=="Setúbal") and (codigo_postal != 2900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Setúbal. Quereria dizer 2900?")

        elif ((cidade=="Viana do Castelo") and (codigo_postal != 4900)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viana do Castelo. Quereria dizer 4900?")

        elif ((cidade=="Vila Real") and (codigo_postal != 5000)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Vila Real. Quereria dizer 5000?")

        elif ((cidade=="Viseu") and (codigo_postal != 3500)):
            raise forms.ValidationError("O código postal que inseriu não corresponde com a cidade de Viseu. Quereria dizer 3500?")

        else:
            return codigo_postal



class ZonaModelForm(forms.ModelForm):
    numero_da_zona = forms.IntegerField(
        required=True,
        initial=1,
        min_value=1,
        max_value=1000
        )
    lugares = forms.IntegerField(
        required=True,
        initial=1,
        min_value=1,
        max_value=1000
        )
    tipo_de_zona = forms.ChoiceField(
        choices=Zona.make_options(),
        required=True
        )

    class Meta:
        model = Zona
        fields = [
            'numero_da_zona',
            'lugares',
            'tipo_de_zona'
        ]



class LugarModelForm(forms.ModelForm):
    numero_do_lugar = forms.IntegerField(
        required=True,
        initial=1,
        min_value=1,
        max_value=1000
        )
    estado = forms.ChoiceField(
        choices=Lugar.make_options(),
        required=True
        )

    class Meta:
        model = Lugar
        fields = [
            'numero_do_lugar',
            'estado'
        ]



class ReclamacaoModelForm(forms.ModelForm):
    reclamacao = forms.CharField(
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder':'Escreva aqui a sua reclamação'}),
        required=True
        )
    
    class Meta:
        model = Reclamacao
        fields = [
            'reclamacao'
        ]

    # def clean_nome(self, *args, **kwargs):
    #     nome=self.cleaned_data.get("nome")
    #     if "@" in nome:
    #         raise forms.ValidationError("This is not a valid title")
    #     else:
    #         return nome

    #    def clean_email(self, *args, **kwargs):
    #        email=self.cleaned_data.get("email")
    #        if not email.endswith("edu"):
    #            raise forms.ValidationError("This is not a valid email")
    #        return email