# Generated by Django 4.0.2 on 2023-02-21 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_remove_comment_user_comment_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
    ]
