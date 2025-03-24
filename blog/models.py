from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', args=[self.slug])

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
