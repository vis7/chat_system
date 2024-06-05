from django.contrib import admin
from .models import Conversation, Message, ScheduleMessage, RecurrentMessage

# Register your models here.
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(ScheduleMessage)
admin.site.register(RecurrentMessage)
