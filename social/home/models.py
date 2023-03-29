from django.db import models
from django.contrib.auth.models import User



class Post(models.Model):
    body = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.__class__.__name__}-{self.id}-{self.slug}"

