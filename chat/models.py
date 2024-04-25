# messaging/models.py

from django.db import models
from django_celery_beat.models import IntervalSchedule
from accounts.models import User


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')

    def __str__(self):
        return f"{self.id}"


class BaseMessage(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation.id} {self.id} {self.sender.id}"

    class Meta:
        ordering = ['-timestamp']
        abstract = True


class Message(BaseMessage):
    is_forwarded = models.BooleanField(default=False)
    reply_to = models.ForeignKey(
        'self', on_delete=models.SET_NULL, related_name='message_reply_to', null=True, blank=True
    )


class ScheduleMessage(BaseMessage):
    schedule_time = models.DateTimeField()


class RecurrentMessage(BaseMessage):
    DAYS, HOURS, MINUTES, SECONDS, MICROSECONDS = 'days', 'hours', 'minutes', 'seconds', 'micro_seconds'
    PERIOD_CHOICE = (
        (IntervalSchedule.DAYS, DAYS),
        (IntervalSchedule.HOURS, HOURS),
        (IntervalSchedule.MINUTES, MINUTES),
        (IntervalSchedule.SECONDS, SECONDS),
        (IntervalSchedule.MICROSECONDS, MICROSECONDS)
    )

    every = models.IntegerField()
    period = models.CharField(choices=PERIOD_CHOICE, max_length=16)

    def __str__(self):
        return f"{self.every} {self.period}"
