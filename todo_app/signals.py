from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail

@receiver(post_save , sender= User)
def send_welcome_email(sender,instance,created,**kwargs):
    if created:
        send_mail(
            subject="Welcome",
            message=f"Hello {instance.username} to our Todo . Create your todos for your day-to-day work and accomplish all of your tasks",
            from_email="ayushijoshi3010@gmail.com",
            recipient_list=[instance.email]
            )