# If we want to allow users to create their own posts, we must create forms
from django import forms
from .models import Post

class NewPostForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Caption'}), required=True)
    tag = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Tags | Seperate with comma'}))

    class Meta:
        model = Post
        fields = ('image', 'caption', 'tag')
