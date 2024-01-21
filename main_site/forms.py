from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

    class Media:
        js = ('/static/main_site/ckeditor.js',)


class BlogAddForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug']


class AuthenticateWithPasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
