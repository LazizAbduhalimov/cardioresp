# Generated by Django 4.0.2 on 2023-03-01 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0012_comment_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, related_name='tags', to='blogs.Tags', verbose_name='Ключевые слова'),
        ),
    ]
