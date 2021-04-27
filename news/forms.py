from django import forms
from news.models import News, News_comments, News_category


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = [
            'title',
            'image',
            'text',
            'category',
]


class NewsCommentForm(forms.ModelForm):

    class Meta:
        model = News_comments
        fields = [
            'text',
        ]

class CategoryForm(forms.ModelForm):

    class Meta:
        model = News_category
        fields = [
            'name',
        ]