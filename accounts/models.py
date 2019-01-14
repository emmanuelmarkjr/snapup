from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    full_name = models.CharField(max_length=100, default="", blank=True)
    phone = models.CharField(max_length=11, blank=False, default="")
    picture = models.ImageField(upload_to='profile_images', blank=False)
    visit = models.IntegerField(default=0)
    time_added = models.TimeField(auto_now_add=True)
    date_added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class SnapLink(models.Model):
    user = models.CharField(max_length=200, default="")
    snap_link = models.URLField()
    title = models.CharField(max_length=200, default="")
    img_url = models.TextField(default="")
    price = models.CharField(max_length=200, default="")
    currency = models.CharField(max_length=200, default="")
    date_added = models.DateField(auto_now=True)
    time_added = models.TimeField(auto_now=True)
    notify_me_type = models.CharField(max_length=200, default='None')
    percentage = models.CharField(max_length=200, default="", null=True)
    exact_price = models.CharField(max_length=200, default="", null=True)

    def __str__(self):
        return self.snap_link

    class Meta:
        verbose_name_plural = "Snap Links"


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)