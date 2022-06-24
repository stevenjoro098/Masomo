from django.db import models
from django.contrib.auth.models import User
#from courses.models import Course

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='media/profiles', default='media/profiles/default.jpg', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    #course = models.ForeignKey(Course, related_name='user_course', on_delete=models.CASCADE, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.telephone

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def get_absolute_url(self):
        pass
