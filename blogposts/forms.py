from django import forms
from tinymce import TinyMCE
from .models import Post, Comment


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, initial):
        return False


class PostForm(forms.ModelForm):
    body = forms.CharField(
        widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10})
    )

    class Meta:
        model = Post
        fields = ['title', 'overview', 'body', 'thumbnail', 'categories', 'previous_post', 'next_post']


class CommentForm(forms.ModelForm):
    author = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
        'name': 'username',
        'id': 'username',
        'max_length': 30,
    }), label='')
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'name': 'usercomment',
        'id': 'usercomment',
        'style': "height: 20px"
    }), label='')

    class Meta:
        model = Comment
        fields = ['author', 'body']
