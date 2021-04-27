from django.urls import path
from news.views import category, news_add, comments_like, news_detail, com_delete,\
    comments_dislike, news_edit, category_add, news_delete, category_delete, news_list

urlpatterns = [
    path('', news_list, name='news_list'),
    path('category/<int:cat_id>/', category, name='category'),
    path('news_detail/<int:news_id>/', news_detail, name='news_detail'),
    path('news_add/', news_add, name='news_add'),
    path('cat_add/', category_add, name='category_add'),
    path('news_edit/<int:news_id>/', news_edit, name='news_edit'),
    path('news_detail/<int:news_id>/<int:com_id>/', com_delete, name='com_delete'),
    path('news_delete/<int:news_id>/', news_delete, name='news_delete'),
    path('category_delete/<int:cat_id>/', category_delete, name='category_delete'),
    path('news_detail/comments/<int:news_id>/<int:com_id>/like/', comments_like, name='comments_like'),
    path('news_detail/comments/<int:news_id>/<int:com_id>/dis/', comments_dislike, name='comments_dislike'),


]
