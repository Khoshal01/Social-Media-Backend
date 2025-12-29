from home.model import Follow , Like, Comment
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction

# ======================
# Profile creation service
# ======================
class ProfileServices:
    @staticmethod
    def create_profile(user, bio, image=None, is_private=False):
        from home.models import Profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={'bio': bio, 'image': image, 'is_private': is_private}
        )
        return profile


# ======================
# Post Services 
# ======================


class PostServices:
    @staticmethod
    def create_post(*,author,content,media_url= None,privacy):
        from home.model import PostModel 
        
        return PostModel.objects.create(
            author=author,
            content=content,
            privacy=privacy,
            media_url=media_url
        )

# ======================
# Follow / Unfollow signals
# ======================

@receiver(post_save, sender=Follow)
def follow_user(sender, instance, created, **kwargs):
    if created:
        # Increment following/follower counts
        instance.follower.profile.following_count += 1
        instance.follower.profile.save()

        instance.following.profile.followers_count += 1
        instance.following.profile.save()


@receiver(post_delete, sender=Follow)
def unfollow_user(sender, instance, **kwargs):
    # Decrement following/follower counts
    instance.follower.profile.following_count -= 1
    instance.follower.profile.save()

    instance.following.profile.followers_count -= 1
    instance.following.profile.save()



class LikeService:

    @staticmethod
    @transaction.atomic
    def like_post(user_profile, post):
        """
        Like a post if not already liked
        """
        like= Like.objects.get_or_create(
            user=user_profile,
            post=post
        )
        if like:
            post.likes_count += 1
            post.save(update_fields=['likes_count'])
        return like

    @staticmethod
    @transaction.atomic
    def unlike_post(user_profile, post):
        """
        Remove a like if it exists
        """
        deleted= Like.objects.filter(
            user=user_profile,
            post=post
        ).delete()
        if deleted:
            post.likes_count -= 1
            post.save(update_fields=['likes_count'])


class CommentService:

    @staticmethod
    @transaction.atomic
    def post_comment(user_profile,post,comment):
        comment = Comment.objects.create(
            user = user_profile,
            post = post,
            text = comment
        )
        if comment:
            post.comments_count += 1
            post.save(update_fields=['comments_count'])
        return comment


    @staticmethod
    @transaction.atomic
    def delete_post(user_profile,post):
        delete= Comment.objects.filter(
            user = user_profile,
            post = post
        ).delete()

        if delete:
            post.comments_count -= 1
            post.save(update_fields = ['comments_count'])





