from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # создание стандартной формы с заполнением атрибутов
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    # создание формы на основе готовой модели
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
