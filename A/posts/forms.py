from django import forms
from .models import Post,Comment


class AddPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('body',)


class EditPostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('body',)
class AddCommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets = {
            'body':forms.Textarea(attrs={'cols': 15, 'rows': 5,'class':'form-control'}),
        }
        error_messages = {
            'body': {
                'max_length':"max 400 character .",
                'required':"required.",
            },
        }


class AddReplyForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('body',)
        widgets = {
            'body':forms.Textarea(attrs={'cols': 10, 'rows': 5,'class':'form-control'}),
        }
     