from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    #  определили перечисляемый класс Status путем подклассирования класса models.TextChoices
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')  # slug - только латинские буквы, цифры, знаки подчеркивания или дефисы
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')  # взаимосвязь "многие-к-одному"
    body = models.TextField(default='lalalalalalalalalala')
    publish = models.DateTimeField(default=timezone.now)  # текущие дата и время, зависящие от UTC
    created = models.DateTimeField(auto_now_add=True)  # дата будет сохраняться автоматически во время создания объекта
    updated = models.DateTimeField(auto_now=True)  # дата будет обновляться автоматически во время сохранения объекта
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()  # менеджер, применяемый по умолчанию
    published = PublishedManager()  # конкретно-прикладной менеджер

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]  # позволяет определять в модели индексы БД

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])

    tags = TaggableManager()


class Comment(models.Model):
    # многие-к-одному
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']), ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
