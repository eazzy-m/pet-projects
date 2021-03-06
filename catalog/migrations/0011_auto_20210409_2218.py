# Generated by Django 3.1.7 on 2021-04-09 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('catalog', '0010_delete_specification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods_in_basket',
            name='good',
        ),
        migrations.AddField(
            model_name='goods_in_basket',
            name='content_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goods_in_basket',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Good',
        ),
    ]
