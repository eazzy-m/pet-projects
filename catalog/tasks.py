# Create your tasks here

from celery import shared_task
import requests


@shared_task
def change():
    from .models import Course, MobTel, Television
    url = 'https://www.nbrb.by/api/exrates/rates/145'
    res = requests.get(url).json()['Cur_OfficialRate']
    if not Course.objects.exists():
        cours = Course.objects.create()
        cours.course = res
        cours.save()
    else:
        cours = Course.objects.first()
        cours.course = res
        cours.save()
    models = [MobTel, Television]
    for j in models:
        for i in j._base_manager.all():
            i.price_in_d = float(i.price) / res
            i.save()
    return cours






