# Generated by Django 3.1.7 on 2021-04-25 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0030_auto_20210424_2303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='user',
        ),
    ]