from django.db import models
from django.utils import timezone

# Create your models here.

# 文章
class Article(models.Model):

    author = models.CharField(max_length=16)
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=2000)
    # create_time = models.DateTimeField(default=timezone.now,)
    create_time = models.DateTimeField(auto_now=True)

    @classmethod
    def publish_article(cls, author, title, content):
        art = cls(author=author, title=title, content=content)
        return art

    class Meta:
        ordering = ['-create_time']

# 评论
class BlogComment(models.Model):
    username = models.CharField(max_length=16)
    article = models.ForeignKey(Article)
    comment = models.TextField(max_length=1000)
    parent = models.ForeignKey('self',default=None,blank=True,null=True)
    # create_time = models.DateTimeField(default=timezone.now)
    create_time = models.DateTimeField(auto_now=True)


    @classmethod
    def comment_text(cls, username, article, comment, parent):
        com = cls(username=username, article=article, parent=parent, comment=comment)
        return com
    class Meta:
        ordering = ['-create_time']





