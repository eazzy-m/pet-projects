from django.db import models
from django.urls import reverse


class Topic(models.Model):
    title = models.CharField(max_length=50, db_index=True, verbose_name='Тема')

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('comment_view', kwargs={'topic_id': self.pk})

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


class Comment(models.Model):
    text = models.TextField(max_length=250, verbose_name='Текст')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, verbose_name='Тема обсуждения')
    text_mutual = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='связь с др. комм.')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
