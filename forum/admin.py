from django.contrib import admin
from .models import Topic, Comment


class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'topic', 'created_at', 'text_mutual')
    list_display_links = ('topic', 'created_at')
    search_fields = ('topic', 'author')
    save_on_top = True


admin.site.register(Comment, CommentAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.site_title = 'Управление форумом'
admin.site.site_header = 'Управление форумом'