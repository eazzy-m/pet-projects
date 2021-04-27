from django.shortcuts import render, get_object_or_404, redirect
from news.models import News_category, News, News_comments
from news.forms import NewsForm, NewsCommentForm, CategoryForm
from django.utils import timezone


def news_list(request):
    news = News.objects.all().filter(publish=True)
    cats = News_category.objects.all()
    context = {
        'news': news,
        'cats': cats,
        'cat_selected': 0,
        'title': 'Новости',
    }
    return render(request, 'news/news_list.html', context=context)


def category(request, cat_id):
    cats = News_category.objects.all()
    news = News.objects.filter(category_id=cat_id)
    news_by_views = News.objects.all().filter(category_id=cat_id).order_by('-views')[0:8]
    context = {
        'news': news,
        'cats': cats,
        'cat_selected': cat_id,
        'news_by_views': news_by_views,
    }
    return render(request, 'news/news_list.html', context=context)


def news_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    cats = News_category.objects.all()
    news.views += 1
    news.save()
    if request.method == "POST":
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.news = news
            comment.save()
            return redirect('news_detail', news_id=news_id)
    else:
        form = NewsCommentForm()
    comments = News_comments.objects.filter(news__pk=news_id)
    context = {
        'news': news,
        'cats': cats,
        'comments': comments,
        'form': form,
    }
    return render(request, 'news/news_detail.html', context=context)


def news_add(request):
    cats = News_category.objects.all()
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.published_date = timezone.now()
            news.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm()
    return render(request, 'news/news_add.html', {'form': form, 'cats': cats})


def news_delete(request, news_id):
    cat = News_category.objects.filter(news__id=news_id).get()
    news = News.objects.filter(id=news_id)
    news.delete()
    return redirect('category', cat_id=cat.id)


def category_add(request):
    cats = News_category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.save()
            return redirect('news_list')
    else:
        form = CategoryForm()
    return render(request, 'news/cat_add.html', {'form': form, 'cats': cats})


def category_delete(request, cat_id):
    cat = News_category.objects.filter(id=cat_id)
    cat.delete()
    return redirect('news_list')


def news_edit(request, news_id):
    cats = News_category.objects.all()
    news = get_object_or_404(News, id=news_id)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.published_date = timezone.now()
            news.save()
            return redirect('news_detail', news_id=news.id)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_edit.html', {'form': form, 'cats': cats})


def com_delete(request, news_id, com_id):
    comment = News_comments.objects.filter(id=com_id)
    comment.delete()
    news = get_object_or_404(News, id=news_id)
    return redirect('news_detail', news_id=news.id)


def comments_like(request, news_id, com_id):
    com = News_comments.objects.get(id=com_id)
    com.like += 1
    com.save()
    news = get_object_or_404(News, id=news_id)
    return redirect('news_detail', news_id=news.id)


def comments_dislike(request, news_id, com_id):
    com = News_comments.objects.get(id=com_id)
    com.dislike += 1
    com.save()
    news = get_object_or_404(News, id=news_id)
    return redirect('news_detail', news_id=news.id)
