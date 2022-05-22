# Generated by Django 4.0.2 on 2022-03-30 10:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('parque', '0008_alter_registomovimento_data_de_entrada'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='parque.parque'),
        ),
        migrations.AddField(
            model_name='registomovimento',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='parque.parque'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='parque.parque'),
        ),
        migrations.AddField(
            model_name='reserva',
            name='viaturaid',
            field=models.ForeignKey(db_column='ViaturaID', default=1, on_delete=django.db.models.deletion.CASCADE, to='parque.viatura'),
        ),
    ]