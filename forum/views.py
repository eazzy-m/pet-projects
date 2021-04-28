from django.shortcuts import render, redirect
from .models import Topic, Comment
from .forms import CommForm, TopicForm, UserRegisterForm, UserLoginForm
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Count


class TopicViews(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'forum/topics.html'
    paginate_by = 10
    form = TopicForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TopicViews, self).get_context_data(**kwargs)
        context['title'] = 'Форум'
        context['form'] = self.form
        return context

    def get_queryset(self):
        return Topic.objects.annotate(cnt=Count('comment')).order_by('-pk')


class CommentView(ListView):
    model = Comment
    template_name = 'forum/comments.html'
    context_object_name = 'comments'
    allow_empty = True
    paginate_by = 10
    form = CommForm()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CommentView, self).get_context_data(**kwargs)
        context['title'] = Topic.objects.get(pk=self.kwargs['topic_id'])
        context['form'] = self.form
        context['topic_pk'] = self.kwargs['topic_id']
        return context

    def get_queryset(self):
        return Comment.objects.filter(topic_id=self.kwargs['topic_id'])


def popular(request):
    pop_topics = Topic.objects.annotate(cnt=Count('comment')).order_by('-cnt').filter(cnt__gt=1)
    return render(request, 'forum/popular.html', {'pop_topics': pop_topics, })


def users_topics(request):
    topics = Topic.objects.filter(comment__author=request.user).annotate(cnt=Count('comment'))
    return render(request, 'forum/users_topic.html', {'topics': topics, })


def add_comment(request, topic_pk):
    if request.method == 'POST':
        com = Comment(topic=Topic.objects.get(pk=topic_pk), author=request.user, text=request.POST['text'])
        com.text = com.text.replace(com.text[0], com.text[0].title(), 1)
        com.save()

        return redirect('comment_view', topic_pk,)
    else:
        com = CommForm()
    return render(request, 'forum/comments.html', {'form': com, 'topic_pk': topic_pk})


def add_topic(request):
    if request.method == 'POST':
        new_topic = TopicForm(request.POST)
        if new_topic.is_valid():
            new_topic.save()
            return redirect('topic_view')
    else:
        new_topic = TopicForm()
    return render(request, 'forum/add_topic.html', {'form': new_topic})


def add_mute(request, comment_pk, topic_pk):
    comments = Comment.objects.get(topic_id=topic_pk, pk=comment_pk)
    if request.method == 'POST':
        com = Comment()
        com.author = request.user
        com.text_mutual = Comment.objects.get(pk=comment_pk)
        com.topic = Topic.objects.get(pk=topic_pk)
        com.text = request.POST['text']
        com.text = com.text.replace(com.text[0], com.text[0].title(), 1)
        com.save()
        return redirect('comment_view', topic_pk)
    else:
        com = CommForm()

    return render(request, 'forum/mute.html', {'form': com,
                                               'topic_pk': topic_pk,
                                               'comment_pk': comment_pk,
                                               'comments': comments})


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Произошла ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'forum/register.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
    else:
        form = UserLoginForm()
    return render(request, 'forum/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('main')
