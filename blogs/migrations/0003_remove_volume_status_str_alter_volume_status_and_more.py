# Generated by Django 4.0.2 on 2023-02-20 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volume',
            name='status_str',
        ),
        migrations.AlterField(
            model_name='volume',
            name='status',
            field=models.CharField(blank=True, max_length=100, verbose_name='Строка статуса'),
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]
