from django import forms
from .models import Category, Cosmetic, Like, Comment

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

class CosmeticForm(forms.ModelForm):
    class Meta:
        model = Cosmetic
        fields = ['category', 'title', 'description', 'image', 'price']

class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['cosmetic', 'user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш комментарий...'})
        }
