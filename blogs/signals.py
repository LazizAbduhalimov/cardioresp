from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver

from .models import Article, Tags


@receiver(pre_save, sender=Article)
def create_default_objects(sender, instance, **kwargs):
    tags_title = str(instance.tags_text).replace(" ", "").replace(";", ",").split(",")
    for title in tags_title:
        try:
            tag = Tags.objects.get(title=title)
        except:
            tag = Tags(title=title)
            tag.save()


@receiver(post_save, sender=Article)
def update_tags_number(sender, instance, *args, **kwargs):
    for tag in Tags.objects.all():
        related_articles = Article.objects.filter(tags=tag)
        tag.related_articles_number = related_articles.count()
        if tag.related_articles_number == 0:
            tag.delete()
        else:
            tag.save()
