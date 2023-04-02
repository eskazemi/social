from django import forms
from .models import Post


class UpdateCreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)
