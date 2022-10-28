# blog/models.py
from django.conf import settings
from django.db import models

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # No duplicates!
        null=False,
    )
    slug = models.SlugField(
        unique=True,
        null=False,
    )
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(
        max_length=255,
        null=False,
    )
    content = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',
        null=False,
    )
    created = models.DateTimeField(auto_now_add=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
        null=False,
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    pub = PublishedManager()

    class Meta:
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['created']

    def __str__(self):
        return self.title

class PostManager(models.Manager):
    """
    PostManger to exclude the unchecked check box
    """
    def get_queryset(self):
        queryset = super().get_queryset()  # Get the initial queryset
        return queryset.exclude(approve=False)  # Exclude deleted records

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=100, null=False, default='Please enter email')
    comment = models.TextField(max_length=100)
    approve = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # Updates on each save
    objects = PostManager()

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.comment[:60]
