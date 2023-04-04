from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    body = models.TextField()
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="posts")

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return f"{self.__class__.__name__}-{self.slug}"

    def get_absoluter_url(self):
        return reverse('home:detail', args=(self.id, self.slug))


    def like_counts(self):
        return self.p_votes.count()

    def user_can_like(self, user):
        user_like = user.u_votes.filter(post=self)
        if user_like.exists():
            return True
        else:
            return False



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='u_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='p_comments')
    body = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE,
                              related_name='r_comments', blank=True, null=True)
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.__class__.__name__}-{self.body[:30]}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='u_votes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='p_votes')

    def __str__(self):
        return f"{self.user} liked {self.post.slug}"


