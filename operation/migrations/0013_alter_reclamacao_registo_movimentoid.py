# Generated by Django 4.0.4 on 2022-06-29 21:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0012_reclamacao_registo_movimentoid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reclamacao',
            name='registo_movimentoid',
            field=models.ForeignKey(db_column='Registo-movimentoID', on_delete=django.db.models.deletion.CASCADE, to='operation.registomovimento'),
        ),
    ]