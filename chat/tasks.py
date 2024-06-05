# tasks.py

from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime
from django.utils import timezone

@shared_task
def send_scheduled_message(scheduled_time, schedule_message_id):
    from chat.models import ScheduleMessage, Message
    from chat.serializers import MessageSerializer

    now = timezone.now()

    if now >= scheduled_time:
        # logic for sending message
        schedule_message = ScheduleMessage.objects.filter(id=schedule_message_id).first()

        if schedule_message:
            message_data = {
                "content": schedule_message.content,
                "conversation": schedule_message.conversation.id,
                "sender": schedule_message.sender.id
            }

            serializer = MessageSerializer(data=message_data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                schedule_message.delete()

    else:
        send_scheduled_message.apply_async(args=[scheduled_time, schedule_message_id], eta=scheduled_time)


@shared_task
def recurrent_messge_task(recurrent_message_id):
    from chat.models import RecurrentMessage
    from chat.serializers import MessageSerializer

    recurrent_messge = RecurrentMessage.objects.filter(id=recurrent_message_id).first()

    message_data = {
        "content": recurrent_messge.content,
        "conversation": recurrent_messge.conversation.id,
        "sender": recurrent_messge.sender.id
    }

    serializer = MessageSerializer(data=message_data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()

    return
