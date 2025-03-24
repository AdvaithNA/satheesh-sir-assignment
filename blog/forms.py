from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Category
from django.utils.text import slugify

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'category', 'content', 'status', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        if not post.slug:
            post.slug = slugify(post.title)
        if commit:
            post.save()
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            })
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def save(self, commit=True):
        category = super().save(commit=False)
        if not category.slug:
            category.slug = slugify(category.name)
        if commit:
            category.save()
        return category 