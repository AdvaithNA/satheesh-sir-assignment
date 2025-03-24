from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
)
from django.urls import reverse_lazy
from .models import Post, Category, Comment
from .forms import UserRegistrationForm, PostForm, CommentForm, CategoryForm
from django.core.paginator import Paginator

def index(request):
    """Main entry point for the blog."""
    # Get all published posts
    posts = Post.objects.filter(status='published').order_by('-published_at')
    categories = Category.objects.all()
    
    # Add pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    # Add debugging information
    print(f"Total posts: {Post.objects.count()}")
    print(f"Published posts: {Post.objects.filter(status='published').count()}")
    
    context = {
        'posts': posts,
        'categories': categories,
        'is_paginated': True,
    }
    
    return render(request, 'blog/post_list.html', context)

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'blog/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, 'Successfully logged in!')
        return reverse_lazy('blog:post_list')

class RegisterView(FormView):
    template_name = 'blog/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('blog:post_list')
    
    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            messages.success(self.request, 'Registration successful!')
        return super().form_valid(form)

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    ordering = ['-published_at']

    def get_queryset(self):
        queryset = Post.objects.all()
        category_slug = self.kwargs.get('category_slug')
        
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=self.category)
            print(f"Category found: {self.category.name}")
            print(f"Posts in category: {queryset.count()}")
        
        return queryset.order_by('-published_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        if hasattr(self, 'category'):
            context['category'] = self.category
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'published'  # Ensure post is published
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, slug=self.kwargs['slug'])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, 'Comment added successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail', kwargs={'slug': self.kwargs['slug']})

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/category_form.html'
    success_url = reverse_lazy('blog:category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Category created successfully!')
        return super().form_valid(form)
