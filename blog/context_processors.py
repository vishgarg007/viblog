# blog/context_processors.py
from django.db.models import Count
from . import models


def base_context(request):
    authors = models.Post.objects.published() \
        .get_authors() \
        .order_by('first_name')

    topicside = models.Post.objects.values_list('topics__name') \
        .annotate(dcount=Count('id')) \
        .order_by('-dcount')[:5]

    return {'authors': authors, 'topicside': topicside}
