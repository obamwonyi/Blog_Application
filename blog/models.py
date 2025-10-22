from django.db import models
from django.utils import timezone
from django.conf import settings


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Post.Status.PUBLISHED)
        )

class Post(models.Model):
    """
    Post model
    """

    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    title = models.CharField(max_length=250) # Translate to VARCHAR column in sql
    slug = models.SlugField(max_length=250) # Translate to VARCHAR column in sql
    body = models.TextField() # Translate to TEXT column in sql
    publish = models.DateTimeField(default=timezone.now) # Todo: add the db form
    created = models.DateTimeField(auto_now_add=True) # Todo: add the db form
    updated = models.DateTimeField(auto_now=True) # Todo: add the db form
    status = models.CharField(
        max_length=2,
        choices=Status,
        default=Status.DRAFT,
    )

    class Meta:
        # this only acts when no order is specified,
        # so it's like a default order the sorting is to occur
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        # Say you instantiate post before saving and run
        # print(post), you get the value of the title as the
        # output.
        return self.title