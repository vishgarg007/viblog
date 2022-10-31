# tests/blog/models/test_post.py

from model_mommy import mommy
import pytest
import datetime as dt
from freezegun import freeze_time

from blog.models import Post

# Mark this test module as requiring the database
pytestmark = pytest.mark.django_db


def test_published_posts_only_returns_those_with_published_status():
    # Create a published Post by setting the status to "published"
    published = mommy.make('blog.Post', status=Post.PUBLISHED)
    # Create a draft Post
    mommy.make('blog.Post', status=Post.DRAFT)

    # We expect only the "publised" object to be returned
    expected = [published]
    # Cast the result as a list so we can compare apples with apples!
    # Lists and querysets are of different types.
    result = list(Post.objects.published())

    assert result == expected

def test_publish_sets_status_to_published():
    post = mommy.make('blog.Post', status=Post.DRAFT)
    post.publish()
    assert post.status == Post.PUBLISHED

@freeze_time(dt.datetime(2030, 6, 1, 12), tz_offset=0)  # Replaces now()
def test_publish_sets_published_to_current_datetime():
    # Create a new post, and ensure no published datetime is set
    post = mommy.make('blog.Post', published=None)
    post.publish()

    # Set the timezone to UTC (to match tz_offset=0)
    assert post.published == dt.datetime(2030, 6, 1, 12, tzinfo=dt.timezone.utc)

def test_get_authors_returns_users_who_have_authored_a_post(django_user_model):
    # Create a user
    author = mommy.make(django_user_model)
    # Create a post that is authored by the user
    mommy.make('blog.Post', author=author)
    # Create another user – but this one won't have any posts
    mommy.make(django_user_model)

    assert list(Post.objects.get_authors()) == [author]


def test_authors_included_in_context_data(client, django_user_model):
    """
    Checks that a list of unique published authors is included in the
    context and is ordered by first name.
    """
    # Make a published author called Cosmo
    cosmo = mommy.make(
        django_user_model,
        username='ckramer',
        first_name='Cosmo',
        last_name='Kramer'
    )
    mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=cosmo,
        _quantity=2
    )
    # Make a published author called Elaine
    elaine = mommy.make(
        django_user_model,
        username='ebenez',
        first_name='Elaine',
        last_name='Benez'
    )
    mommy.make(
        'blog.Post',
        status=Post.PUBLISHED,
        author=elaine,
    )

    # Make an unpublished author
    unpublished_author = mommy.make(
        django_user_model,
        username='gcostanza'
    )
    mommy.make('blog.Post', author=unpublished_author, status=Post.DRAFT)

    # Expect Cosmo and Elaine to be returned, in this order
    expected = [cosmo, elaine]

    # Make a request to the home view
    response = client.get('/')

    # The context is available in the test response.
    result = response.context.get('authors')

    # Cast result (QuerySet) to a list to compare
    assert list(result) == expected
