from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= "profile"
    )

    bio = models.TextField()
    image = models.ImageField(upload_to='profile/',null=True,blank=True)

    followers_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)

    is_private = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username 


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'followers_set'
    )

    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name= 'following_set'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta :
        unique_together = ('follower', 'following') 

    
    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"
    



class PostModel(models.Model):
    author = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='author'
    )

    content = models.TextField(max_length=500)
    media_url = models.URLField(null= True, blank= True )

    PRIVACY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
        ('followers', 'Followers'),
    ]

    privacy = models.CharField(
        max_length=20,
        choices=PRIVACY_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    likes_count = models.PositiveIntegerField(default= 0)

    comments_count = models.PositiveIntegerField(default= 0 )


    def __str__(self):
        return  f"Post by {self.author.user.username}"
    
class Like(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)




