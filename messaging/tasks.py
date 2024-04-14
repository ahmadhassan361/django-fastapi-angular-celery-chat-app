# app/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings
from .models import ChatRoomParticipant

@shared_task
def send_message_emails(room_name, message):

    print("its working",room_name,message)
    
    participents = ChatRoomParticipant.objects.filter(room__name=room_name)
    recipent_list = []
    for user in participents:
        recipent_list.append(user.user.username)
        
    subject = 'new message in your inbox'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = recipent_list
    # send_mail( subject, message, email_from, recipient_list ) #this function will send the email to all the recipents