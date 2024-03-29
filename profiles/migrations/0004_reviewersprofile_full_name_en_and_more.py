# Generated by Django 4.0.2 on 2023-02-21 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_authorsprofile_user_reviewersprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewersprofile',
            name='full_name_en',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия'),
        ),
        migrations.AddField(
            model_name='reviewersprofile',
            name='full_name_ru',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия'),
        ),
        migrations.AddField(
            model_name='reviewersprofile',
            name='full_name_uz',
            field=models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия'),
        ),
    ]
