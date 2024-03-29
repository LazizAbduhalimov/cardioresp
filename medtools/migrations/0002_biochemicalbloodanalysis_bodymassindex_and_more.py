# Generated by Django 4.0.2 on 2023-06-02 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medtools', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiochemicalBloodAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ALAT', models.FloatField(default=0, verbose_name='АЛАТ')),
                ('ACAT', models.FloatField(default=0, verbose_name='АСАТ')),
                ('creotenin', models.FloatField(default=0, verbose_name='Креотенин')),
                ('urea', models.FloatField(default=0, verbose_name='Мочевина')),
                ('uric_acid', models.FloatField(default=0, verbose_name='Мочевая кислота')),
                ('bilirubin_common', models.FloatField(default=0, verbose_name='Билурибин общий')),
                ('bilirubin_direct', models.FloatField(default=0, verbose_name='Билурибин прямой')),
                ('bilirubin_indirect', models.FloatField(default=0, verbose_name='Билурибин непрямой')),
                ('glucose', models.FloatField(default=0, verbose_name='Глюкоза (кровь)')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='BodyMassIndex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField(default=0, verbose_name='Рост')),
                ('mass', models.FloatField(default=0, verbose_name='Mass')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='CoronaryAngiography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4+')], default='', max_length=1, verbose_name='')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='ECG',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field', models.CharField(choices=[('ST_1', 'Подъём сегманта ST'), ('ST_2', 'Депрессия сегманта ST'), ('T', 'Инверсия зубца T')], default='', max_length=4, verbose_name='')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='Echocardiography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ejection_fraction', models.FloatField(default=0, verbose_name='ФВЛЖ (%)')),
                ('end_systolic_size', models.FloatField(default=0, verbose_name='КСР (см)')),
                ('eslj', models.FloatField(default=0, verbose_name='ЭСЛЖ (см)')),
                ('mjp', models.FloatField(default=0, verbose_name='МЖП (см)')),
                ('pj', models.FloatField(default=0, verbose_name='ПЖ (см)')),
                ('mk', models.CharField(choices=[('not th', 'Не уплотнённый'), ('th', 'Уплотнённый')], default='', max_length=6, verbose_name='МК (см)')),
                ('lp', models.FloatField(default=0, verbose_name='ЛП (см)')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='GeneticResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IL_1b_511_TC', models.CharField(choices=[('C/C', 'C/C'), ('C/T', 'C/T'), ('T/T', 'T/T')], default='', max_length=3, verbose_name='IL-1b 511 T/C')),
                ('IL_10_819_CT', models.CharField(choices=[('C/C', 'C/C'), ('C/T', 'C/T'), ('T/T', 'T/T')], default='', max_length=3, verbose_name='IL-10 819 C/T')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='ImmunologicalResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IL_1b', models.FloatField(default=0, verbose_name='IL-1(b)')),
                ('TNF_a', models.FloatField(default=0, verbose_name='TNF-a')),
                ('IL_4', models.FloatField(default=0, verbose_name='IL-4')),
                ('IL_10', models.FloatField(default=0, verbose_name='IL-10')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.CreateModel(
            name='pilidogram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HS', models.FloatField(default=0, verbose_name='Общий ХС ммоль/г')),
                ('HS_LLNP', models.FloatField(default=0, verbose_name='ХС ЛЛНП. ммоль/г')),
                ('HS_LLVP', models.FloatField(default=0, verbose_name='ХС ЛЛВП. ммоль/г')),
                ('TG', models.FloatField(default=0, verbose_name='ТГ. ммоль/г')),
                ('KAT', models.FloatField(default=0, verbose_name='КАТ')),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='medtools.patient', verbose_name='Пациент')),
            ],
        ),
        migrations.RemoveField(
            model_name='component',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='intfielditem',
            name='component',
        ),
        migrations.DeleteModel(
            name='ChoiceFieldItem',
        ),
        migrations.DeleteModel(
            name='Component',
        ),
        migrations.DeleteModel(
            name='IntFieldItem',
        ),
    ]
