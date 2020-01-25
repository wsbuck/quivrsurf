from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.core.mail import send_mail

from decouple import config, Csv

from .models import User

def send_welcome_email(new_user_pk):
    """
    Sends email to a new user
    """
    host = config('HOST')
    new_user = User.objects.get(pk=new_user_pk)
    subject = "Welcome! Please activate your account"
    to_email = [new_user.email]
    from_email = 'noreply@quivrsurf.com'
    
    activation_link = host + new_user.create_activation_link()
    body = "Please click {} to activate.".format(activation_link)
    send_mail(subject, body, from_email, to_email)



@receiver(post_save, sender=User)
def send_email_message(sender, instance, created, **kwargs):
    if created:
        send_welcome_email(instance.pk)
