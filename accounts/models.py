import random
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

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
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    image = models.ImageField(default='default.png',upload_to='profile_pics')
    nickname = models.CharField(max_length=11,blank=True,null=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(blank=True, null=True)



