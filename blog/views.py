from django.views import View
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse
from .models import Post, Comment, PostManager, Topic, PostQueryset
from .forms import CommentForm
from django.shortcuts import render
from . import models
from django.db.models import Count

def home(request):
    """
    The Blog homepage
    """
    latest_posts = models.Post.objects.published().order_by('-published')[:5]
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Post.objects.values('topics').annotate(dcount=Count('id')).order_by('-dcount')

    context = {
        'authors': authors,
        'latest_posts': latest_posts,
        'topics': topics,
    }

    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

class PostDisplay(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

class PostComment(SingleObjectMixin, FormView):
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostComment, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse('blog/post_detail', kwargs={'pk': post.pk}) + '#comments'

class PostDetailView(View):

    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostComment.as_view()
        return view(request, *args, **kwargs)
