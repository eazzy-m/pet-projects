from django.urls import path
from .views import TopicViews, CommentView, add_comment, add_mute, popular, add_topic, register, user_login, user_logout, users_topics

urlpatterns = [
    path('', TopicViews.as_view(), name='topic_view'),
    path('comments/<int:topic_id>', CommentView.as_view(), name='comment_view'),
    path('add_comment/<int:topic_pk>', add_comment, name='add_comment'),
    path('add_mute/<int:comment_pk>/<int:topic_pk>', add_mute, name='add_mute'),
    path('popular/', popular, name='popular'),
    path('add_topic/', add_topic, name='add_topic'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('users_topic/', users_topics, name='users_topic')
]
