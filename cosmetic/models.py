from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _



class Category(models.Model):
    name = models.CharField(_('name'),max_length=100)
    image=models.ImageField()
    def __str__(self):
        return self.name

class Cosmetic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cosmetics')
    title = models.CharField(_('title'),max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='cosmetic_images/')
    price = models.DecimalField(_('price'),max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        'accounts.CustomUser',  # ← строковая ссылка на модель
        on_delete=models.CASCADE,
        null=True,  # временно
        blank=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    recommendations = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='recommended_for')

    def __str__(self):
        return self.title

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.count()

class Like(models.Model):
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # теперь привязано к CustomUser
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Like by {self.user.username} on {self.cosmetic.title}"

class Comment(models.Model):
    cosmetic = models.ForeignKey(Cosmetic, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # <-- вот так
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Comment by {self.user.username} on {self.cosmetic.title}"

