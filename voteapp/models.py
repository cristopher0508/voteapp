from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=500, blank=True)
    picture = models.ImageField(upload_to='upload/profile_pictures', default='upload/default.png')
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,  related_name='profile', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class voteImages(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=500, blank=True)
    first_image = models.ImageField(upload_to='upload/votes_images')
    second_image = models.ImageField(upload_to='upload/votes_images')
    vote_image_first = models.ManyToManyField(UserProfile, blank=True, related_name='vote_one')
    vote_image_second = models.ManyToManyField(UserProfile, blank=True,  related_name='vote_second')
    vote_count_first = models.IntegerField(default=0)
    vote_count_second = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='vote')


    def count_image_first(self):
        return self.vote_image_first.count()
    
    def count_image_first(self):
        return self.vote_image_second.count()
    
    def total_votes(self):
        return int(self.vote_image_first.count()) + int(self.vote_image_second.count())
    


class Notification(models.Model):
    #1 = Vote #2=follow
    notification_type = models.IntegerField(null=True, blank=True)
    to_user = models.ForeignKey(UserProfile, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_user = models.ForeignKey(UserProfile, related_name='notification_from', on_delete=models.CASCADE, null=True)
    vote = models.ForeignKey(voteImages, on_delete=models.CASCADE, related_name="+", null=True, blank=True)
    user_has_seen = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

  