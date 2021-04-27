from django.urls import reverse
from django.db import models


class News_category(models.Model):
    name = models.CharField(max_length=16, db_index=True, verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, upload_to='media/', verbose_name='Изображение')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(News_category, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Категория')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    publish = models.BooleanField(default=True)
    sum_comments = models.IntegerField(default=0, verbose_name='Комментарии')
    rating = models.IntegerField(default=0, verbose_name='Pейтинг')

    def __str__(self):
        return f'{self.title}'

    @property
    def count(self):
        self.sum_comments = News_comments.objects.filter(news=self).count()
        return self.sum_comments

    def get_absolute_url(self):
        return reverse('news_detail',  kwargs={'news_id': self.pk})


class News_comments(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Автор')
    text = models.TextField(verbose_name='Текст')
    created_date = models.DateTimeField(auto_now_add=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Новость')
    like = models.IntegerField(default=0, verbose_name='like')
    dislike = models.IntegerField(default=0, verbose_name='dislike')


    def __str__(self):
        return f'{self.text}'

