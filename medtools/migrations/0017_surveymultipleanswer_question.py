# Generated by Django 4.0.2 on 2023-06-08 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medtools', '0016_remove_surveymultipleanswer_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveymultipleanswer',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='medtools.surveyquestion', verbose_name='Пациент'),
        ),
    ]
