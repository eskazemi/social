from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    body=models.TextField(max_length=400)
    slug=models.SlugField(max_length=200)
    create=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}-{self.body[:30]}'

    def get_absolute_url(self):
        return reverse('posts:detail_post', args=[self.create.year,self.create.month,
        self.create.day,self.slug])

class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='ucomment')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='pcomment')
    reply=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True,related_name='rcomment')
    is_reply=models.BooleanField(default=False)
    body=models.TextField(max_length=400)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.body[:30]}'

    class Meta:
        ordering=('-created',)