from django.db import models

# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=32, verbose_name='Город')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
