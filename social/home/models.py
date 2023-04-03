from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    body = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")


    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"{self.__class__.__name__}-{self.slug}"

    def get_absoluter_url(self):
        return reverse('home:detail', args=(self.id, self.slug))
