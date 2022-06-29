# Generated by Django 4.0.4 on 2022-06-28 21:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0010_alter_lugar_zonaid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fatura',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('nomeEmpresa', models.TextField(db_column='NomeEmpresa')),
                ('moradaEmpresa', models.TextField(db_column='MoradaEmpresa')),
                ('nifEmpresa', models.IntegerField(blank=True, db_column='NIFEmpresa', null=True)),
                ('clienteid', models.ForeignKey(blank=True, db_column='ClienteID', null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.cliente')),
                ('pagamentoid', models.ForeignKey(blank=True, db_column='PagamentoID', null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.pagamento')),
            ],
        ),
        migrations.CreateModel(
            name='Reclamacao',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('reclamacao', models.CharField(blank=True, db_column='Reclamacao', max_length=255, null=True)),
                ('faturaid', models.ForeignKey(blank=True, db_column='FaturaID', null=True, on_delete=django.db.models.deletion.CASCADE, to='operation.fatura')),
            ],
        ),
    ]