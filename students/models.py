from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile', on_delete=models.CASCADE)
    telephone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media/profiles')
    created = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, related_name='user_course', on_delete=models.CASCADE)

    def __str__(self):
        return self.telephone


    def get_absolute_url(self):
        pass
