# Generated by Django 4.0.3 on 2022-03-31 14:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.parque'),
        ),
        migrations.AlterField(
            model_name='registomovimento',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.parque'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='parqueid',
            field=models.ForeignKey(db_column='ParqueID', default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.parque'),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='viaturaid',
            field=models.ForeignKey(db_column='ViaturaID', default=1, on_delete=django.db.models.deletion.CASCADE, to='operation.viatura'),
        ),
    ]
