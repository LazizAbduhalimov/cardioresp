# Generated by Django 4.0.2 on 2023-05-31 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255, verbose_name='Имя')),
                ('sex', models.CharField(choices=[('M', 'Мужчина'), ('W', 'Женщина')], default='M', max_length=1, verbose_name='Пол')),
                ('age', models.CharField(choices=[('<60', 'Старше 60'), ('>60', 'Младше 60')], default='', max_length=3, verbose_name='Возраст')),
                ('congestive_heart_failure', models.BooleanField(default=False, verbose_name='ОСН')),
                ('chronic_heart_failure', models.BooleanField(default=False, verbose_name='ХСН')),
                ('heart_rhythm_disturbances', models.BooleanField(default=False, verbose_name='Нарушение ритма')),
                ('congestive_pneumonia', models.BooleanField(default=False, verbose_name='Застойчивая пневмония')),
                ('underlying_disease', models.BooleanField(default=False, verbose_name='Фоновое заболевание')),
                ('social_position', models.CharField(choices=[('S', 'Удовлетворительно'), ('D', 'Неудовлетворительно')], default='', max_length=1, verbose_name='Социальное положение')),
                ('pain_duration', models.CharField(choices=[('L20M', 'Менее 20 минут'), ('M20M', 'Более 20 минут'), ('M24H', 'Более 24 часов')], default='', max_length=4, verbose_name='Продолжительность боли')),
            ],
        ),
        migrations.CreateModel(
            name='IntFieldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_value', models.FloatField(default=0, verbose_name='Вводимое значение')),
                ('normalized_value', models.FloatField(default=0, verbose_name='Норма значения')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medtools.component', verbose_name='Компонент')),
            ],
        ),
        migrations.AddField(
            model_name='component',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент'),
        ),
        migrations.CreateModel(
            name='ChoiceFieldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_value', models.FloatField(default=0, verbose_name='Вводимое значение')),
                ('normalized_value', models.FloatField(default=0, verbose_name='Норма значения')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medtools.component', verbose_name='Компонент')),
            ],
        ),
    ]
