from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save

# Create your models here.

class User(AbstractUser):
    username=models.CharField(max_length=50,unique=True)
    email=models.EmailField(max_length=100, unique=True)

    REQUIRED_FIELDS=['username']
    USERNAME_FIELD='email'

    def profile(self):
        profile=Profile.objects.get(user=self)

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio=models.TextField(max_length=1000)
    image=models.ImageField(upload_to='profile', blank=True)
    verified=models.BooleanField(default=False)
    full_name=models.CharField(max_length=100, blank=True)

def created_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(created_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

