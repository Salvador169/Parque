# Generated by Django 4.0.4 on 2022-06-29 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0011_fatura_reclamacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='reclamacao',
            name='registo_movimentoid',
            field=models.ForeignKey(db_column='Registo-movimentoID', default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.registomovimento'),
        ),
    ]
