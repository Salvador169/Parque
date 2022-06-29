# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.urls import reverse
import datetime, time
from django.db import connection, models
import numpy as np
from dateutil.relativedelta import relativedelta
    


class Parque(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True)  # Field name made lowercase.
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    zonas = models.IntegerField(db_column='Zonas')  # Field name made lowercase.


class Administrador(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permissao = models.IntegerField(db_column='Permissao')  # Field name made lowercase.


class Cliente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nif = models.IntegerField(db_column='NIF', blank=True, null=True)  # Field name made lowercase.
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_nascimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de nascimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telemovel = models.CharField(db_column='Telemovel', max_length=255, blank=True, null=True)  # Field name made lowercase.

class Periodicidade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    periodicidade = models.CharField(db_column='Periodicidade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    horario = models.CharField(db_column='Horario', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Dia(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Dia', max_length=255, blank=True, null=True)  # Field name made lowercase.
    periodicidadeid = models.ForeignKey(Periodicidade, models.CASCADE, db_column='Periodicidade', default=1)  # Field name made lowercase.


class Contrato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    clienteid = models.ForeignKey(Cliente, models.CASCADE, db_column='ClienteID', default=1)  # Field name made lowercase.
    periodicidadeid = models.ForeignKey(Periodicidade, models.CASCADE, db_column='PeriodicidadeID', default=1)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_inicio = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    valido = models.BooleanField(db_column='Valido', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def get_absolute_url(self):
        return reverse('contrato:contrato-detail', kwargs={'id': self.id})
    
    def getParque(self):
        return Parque.objects.filter(id=self)

    @staticmethod
    def makeOptions():
        parques = Parque.objects.all()
        options=([(parque.id, parque.nome) for parque in parques])
        return options


class Funcionario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    funcao = models.CharField(db_column='Funcao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permissao = models.IntegerField(db_column='Permissao')  # Field name made lowercase.


class RegistoMovimento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    data_de_entrada = models.DateTimeField(default=datetime.datetime.now, db_column='Data de entrada', blank=False, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_saida = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de saida', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    provas = models.CharField(db_column='Provas', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Viatura(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID')  # Field name made lowercase.
    registo_movimentoid = models.ForeignKey(RegistoMovimento, models.CASCADE, db_column='Registo-movimentoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    marca = models.CharField(db_column='Marca', max_length=255, blank=True, null=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='Modelo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Zona(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    numero_da_zona = models.IntegerField(db_column='Numero da zona')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lugares = models.IntegerField(db_column='Lugares')  # Field name made lowercase.


class Reserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    viaturaid = models.ForeignKey(Viatura, models.CASCADE, db_column='ViaturaID', default=1)  # Field name made lowercase.
    data_de_inicio = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.



class Lugar(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    zonaid = models.ForeignKey(Zona, models.CASCADE, db_column='ZonaID')  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True, null=True)  # Field name made lowercase.
    viaturaid = models.ForeignKey(Viatura, models.CASCADE, db_column='ViaturaID', blank=True, null=True)  # Field name made lowercase.
    reservaid = models.ForeignKey(Reserva, models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    numero_do_lugar = models.IntegerField(db_column='Numero do lugar')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)  # Field name made lowercase.

    @staticmethod
    def makeOptions():
        lugares = Lugar.objects.filter(contratoid__isnull=True).filter(reservaid__isnull=True)
        options=([(lugar.id, lugar.numero_do_lugar) for lugar in lugares])
        return options


class Pagamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True, null=True)  # Field name made lowercase.
    reservaid = models.ForeignKey(Reserva, models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    registoid = models.ForeignKey(RegistoMovimento, models.CASCADE, db_column='RegistoID', blank=True, null=True)  # Field name made lowercase.
    montante = models.FloatField(db_column='Montante')  # Field name made lowercase.
    estado_do_pagamento = models.TextField(db_column='Estado do pagamento')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    data_de_vencimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de vencimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    comprovativo = models.FileField(blank=True, null=True)

class Fatura(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    pagamentoid = models.ForeignKey(Pagamento, models.CASCADE, db_column='PagamentoID', blank=True, null=True)  # Field name made lowercase.
    clienteid = models.ForeignKey(Cliente, models.CASCADE, db_column='ClienteID', blank=True, null=True)  # Field name made lowercase.
    nomeEmpresa = models.TextField(db_column='NomeEmpresa')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    moradaEmpresa = models.TextField(db_column='MoradaEmpresa')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    nifEmpresa = models.IntegerField(db_column='NIFEmpresa', blank=True, null=True)  # Field name made lowercase.

class Reclamacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    faturaid = models.ForeignKey(Fatura, models.CASCADE, db_column='FaturaID', blank=True, null=True)  # Field name made lowercase.
    reclamacao = models.CharField(db_column='Reclamacao', max_length=255, blank=True, null=True)  # Field name made lowercase.

class TabelaPrecos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    reservaid = models.ForeignKey(Reserva, models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    preco_por_hora = models.FloatField(db_column='Preco por hora')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_por_hora = models.FloatField(db_column='Taxa por hora')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_noturna = models.FloatField(db_column='Taxa noturna')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    taxa_da_multa = models.FloatField(db_column='Taxa da multa')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_dia = models.FloatField(db_column='Preco Contrato Dia')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_diurno = models.FloatField(db_column='Preco Contrato Diurno')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    preco_contrato_noturno = models.FloatField(db_column='Preco Contrato Noturno')  # Field name made lowercase. Field renamed to remove unsuitable characters.

    @staticmethod
    def getDaysContrato(contrato = None, all=True):
        periodicidade = contrato.periodicidadeid
        if all:
            if periodicidade.periodicidade == "diário":
                days = contrato.data_de_termino - contrato.data_de_inicio
            else:
                week = ""
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Segunda-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Terça-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Quarta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Quinta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Sexta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Sábado").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Domingo").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                days = np.busday_count(contrato.data_de_inicio, contrato.data_de_termino, weekmask=week)
        else:
            if periodicidade.periodicidade == "diário":
                if (contrato.data_de_inicio + relativedelta(months=1)) <= contrato.data_de_termino:
                    days = (contrato.data_de_inicio + relativedelta(months=1)) - contrato.data_de_inicio
                else:
                    days = contrato.data_de_termino - contrato.data_de_inicio
                days = days.days
            else:
                week = ""
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Segunda-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Terça-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Quarta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Quinta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Sexta-Feira").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Sábado").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                if Dia.objects.filter(periodicidadeid=periodicidade, nome="Domingo").count() > 0:
                    week = week + "1"
                else:
                    week = week + "0"
                days = np.busday_count(contrato.data_de_inicio, contrato.data_de_inicio + relativedelta(months=1), weekmask=week)
        
        return days

    @staticmethod
    def getHoursReserva(reserva = None):
        days = reserva.data_de_termino - reserva.data_de_inicio
        return days

    @staticmethod
    def getTime(date = None):    
        days = datetime.datetime.now(datetime.timezone.utc) - date
        return days

    @staticmethod
    def getPrice(contrato = None, reserva = None, registo = None, date = None, all=True):
        
        if contrato:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = contrato.parqueid)
            periodicidade = contrato.periodicidadeid
            dias = TabelaPrecos.getDaysContrato(contrato = contrato, all=all)
            if periodicidade.horario == "24H":
                price = dias * tabelaPrecos.preco_contrato_dia
            if periodicidade.horario == "diurno":
                price = dias * tabelaPrecos.preco_contrato_diurno
            if periodicidade.horario == "noturno":
                price = dias * tabelaPrecos.preco_contrato_noturno
        elif reserva:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = reserva.parqueid)
            dias = TabelaPrecos.getHoursReserva(reserva = reserva)
            price = dias.seconds/3600 * tabelaPrecos.preco_por_hora
        else:
            tabelaPrecos = TabelaPrecos.objects.get(parqueid = registo.parqueid)
            dias = TabelaPrecos.getTime(date = registo.data_de_entrada)
            price = dias.seconds/3600 * tabelaPrecos.preco_por_hora
        return "{:.2f}".format(price)