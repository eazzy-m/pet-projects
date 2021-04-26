from django.contrib import admin
from news.models import News_category, News_comments, News


admin.site.register(News_category)
admin.site.register(News)
admin.site.register(News_comments)
