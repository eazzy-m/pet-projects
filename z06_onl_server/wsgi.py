"""
WSGI config for z06_onl_server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import requests


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'z06_onl_server.settings')

application = get_wsgi_application()


def weather():
    url = 'https://www.nbrb.by/api/exrates/rates/145'
    RES = requests.get(url).json()['Cur_OfficialRate']
    print(RES)
    return RES

weather()

