from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'blog'

urlpatterns = [
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='blog:index'), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Main URLs
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    
    # Post URLs
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment URLs
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('category/new/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='category_posts'),
] 