# Generated by Django 3.1.7 on 2021-04-19 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_auto_20210419_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='in_order',
            field=models.BooleanField(default=False),
        ),
    ]
