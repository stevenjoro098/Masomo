from celery import task
from django.core.mail import send_mail
from django.contrib.auth.models import User

@task
def register_sucess(user):
    """ Task to send email whenever New User is Registered..."""
    user = User.objects.get(username='test')
    subject = "Elearning Registration"
    message = 'Dear {0}, \n Thank you for Registering to Elearning. For any Queries or Feedbacks \n Contact Admin'.format(
        'user.first_name')
    mail_sent = send_mail(subject=subject,
                          message=message,
                          from_email='3rdeyesopen@gmail.com',
                          recipient_list=['stevenjoro098@gmail.com'],
                          fail_silently=True)
    return mail_sent
