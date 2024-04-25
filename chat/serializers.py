# messaging/serializers.py

from rest_framework import serializers
from .models import Conversation, Message, ScheduleMessage, RecurrentMessage
from accounts.serializers import UserSerializer


class MessageSerializer(serializers.ModelSerializer):
    # sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class ScheduleMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleMessage
        fields = '__all__'


class RecurrentMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurrentMessage
        fields = '__all__'
