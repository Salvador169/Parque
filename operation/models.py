# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.urls import reverse
from datetime import datetime
from django.db import models


class Parque(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True)  # Field name made lowercase.
    foto = models.CharField(db_column='Foto', max_length=255, blank=True, null=True)
    capacidade = models.IntegerField(db_column='Capacidade')  # Field name made lowercase.
    zonas = models.IntegerField(db_column='Zonas')  # Field name made lowercase.

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nib = models.IntegerField(db_column='NIB', blank=True, null=True)  # Field name made lowercase.
    morada = models.CharField(db_column='Morada', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_nascimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de nascimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telemovel = models.CharField(db_column='Telemovel', max_length=255, blank=True, null=True)  # Field name made lowercase.


class Contrato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    clienteid = models.ForeignKey(Cliente, models.CASCADE, db_column='ClienteID')  # Field name made lowercase.
    data_de_inicio = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.


class Funcionario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    funcao = models.CharField(db_column='Funcao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    permissao = models.IntegerField(db_column='Permissao')  # Field name made lowercase.


class RegistoMovimento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.
    data_de_entrada = models.DateTimeField(default=datetime.now, db_column='Data de entrada', blank=False, null=False)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_saida = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de saida', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    provas = models.CharField(db_column='Provas', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        saida = ""
        if (self.data_de_saida != None):
            saida = self.data_de_saida
        return Parque.__str__(self.parqueid) + ", Matrícula: " + str(self.matricula) + ", Entrada: " + str(self.data_de_entrada) + ", Saída: " + str(self.data_de_saida)

class Viatura(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', null=True)  # Field name made lowercase.
    registo_movimentoid = models.ForeignKey(RegistoMovimento, models.CASCADE, db_column='Registo-movimentoID')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    marca = models.CharField(db_column='Marca', max_length=255, blank=True, null=True)  # Field name made lowercase.
    modelo = models.CharField(db_column='Modelo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return str(self.matricula)

class Zona(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID')  # Field name made lowercase.
    numero_da_zona = models.IntegerField(db_column='Numero da zona')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    lugares = models.IntegerField(db_column='Lugares')  # Field name made lowercase.

    def __str__(self):
        return "Numero da zona: " + str(self.numero_da_zona) + ", Parque: " + str(self.parqueid)


class Reserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Parque, models.CASCADE, db_column='ParqueID', default=1)  # Field name made lowercase.
    viaturaid = models.ForeignKey(Viatura, models.CASCADE, db_column='ViaturaID', default=1)  # Field name made lowercase.
    data_de_inicio = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de inicio', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    data_de_termino = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de termino', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.


class Lugar(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    zonaid = models.ForeignKey(Zona, models.CASCADE, db_column='ZonaID', blank=True, null=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True, null=True)  # Field name made lowercase.
    viaturaid = models.ForeignKey(Viatura, models.CASCADE, db_column='ViaturaID', blank=True, null=True)  # Field name made lowercase.
    reservaid = models.ForeignKey(Reserva, models.CASCADE, db_column='ReservaID', blank=True, null=True)  # Field name made lowercase.
    numero_do_lugar = models.IntegerField(db_column='Numero do lugar')  # Field name made lowercase. Field renamed to remove unsuitable characters.
    estado = models.CharField(db_column='Estado', max_length=255, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return "Lugar: " + str(self.numero_do_lugar) + ", Zona " + str(self.zonaid) + ", Estado: " + str(self.estado)


class Pagamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID')  # Field name made lowercase.
    viaturaid = models.ForeignKey(Viatura, models.CASCADE, db_column='ViaturaID', blank=True, null=True)  # Field name made lowercase.
    montante = models.FloatField(db_column='Montante')  # Field name made lowercase.
    estado_do_pagamento = models.TextField(db_column='Estado do pagamento')  # Field name made lowercase. Field renamed to remove unsuitable characters. This field type is a guess.
    data_de_vencimento = models.DateTimeField(auto_now=False, auto_now_add=False, db_column='Data de vencimento', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.


class TabelaMatriculas(models.Model):
    pais = models.CharField(db_column='Pais', max_length=255)
    formato = models.CharField(db_column='Formato', max_length=255)

    def __str__(self):
        return "País: " + str(self.pais) + ", Formato: " + str(self.formato)


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
    registo_movimentoid = models.ForeignKey(RegistoMovimento, models.CASCADE, db_column='Registo-movimentoID', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    reclamacao = models.CharField(db_column='Reclamacao', max_length=255, blank=True, null=True)  # Field name made lowercase.
