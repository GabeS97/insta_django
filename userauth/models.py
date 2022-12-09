from django.db import models
from django.contrib.auth.models import User
from post.models import Post
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite = models.ManyToManyField(Post)

    def __str__(self):
        return self.user.username
