# Generated by Django 4.0.2 on 2023-06-06 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medtools', '0009_remove_surveyanswer_user_surveyanswer_patient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveyanswer',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент'),
        ),
    ]
