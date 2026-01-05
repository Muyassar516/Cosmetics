import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from cosmetic.models import Cosmetic
from django.conf import settings

class RoleChoice(models.TextChoices):
    ADMIN=('admin','Admin')
    PUBLISHER=('publisher','Publisher')
    READER=('reader','Reader')

class CustomUser(AbstractUser):

    phone_number = models.CharField(max_length=11,blank=True,null=True)
    role = models.CharField(max_length=50, choices=RoleChoice.choices, default=RoleChoice.READER)


def code_generate():
    return str(random.randint(100000,999999))


def get_expire_time():
    return timezone.now()+timedelta(minutes=2)
class Code(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    code=models.CharField(max_length=6)
    expire_date=models.DateField(default=get_expire_time)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    nickname = models.CharField(max_length=11, blank=True, null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)
    favorites = models.ManyToManyField(Cosmetic, blank=True, related_name='favorited_by')

    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()





