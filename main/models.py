from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, default="No bio yet")
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # likes ManyToManyField মুছে দাও এখানে

    def __str__(self):
        return f"{self.author.username} - {self.created_at}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')  # related_name ঠিক আছে
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now) 

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follow_follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='follow_following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)