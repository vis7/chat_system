from django.db.models import Count
from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from accounts.models import User
from .models import Conversation, Message, ScheduleMessage, RecurrentMessage
from .serializers import MessageSerializer, ScheduleMessageSerializer, RecurrentMessageSerializer
from .tasks import send_scheduled_message


class FetchConversationView(APIView):
    def post(self, request, *args, **kwargs):
        receiver_phone_number = request.data.get('phone_number')
        receiver = User.objects.filter(phone_number=receiver_phone_number).first()

        if not receiver:
            data = {"message": "receiver mobile number not found"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.annotate(
                num_participants=Count("participants")
        ).filter(
                num_participants=2, participants__in=[request.user, receiver]
        ).first()

        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(request.user, receiver)

        data = {
            "conversation": conversation.id
        }
        return Response(data, status=status.HTTP_200_OK)


class SendMessageView(APIView):
    def post(self, request, *args, **kwargs):
        message = request.data.get('message', '')
        conversation = request.data.get('conversation', '')
        reply_to = request.data.get('reply_to', None)

        if not message or not conversation:
            data = {"message": "message and conversation id are required"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        message_data = {
            "conversation": conversation,
            "content": message,
            "sender": request.user.id,
            "reply_to": reply_to,
        }

        serializer =  MessageSerializer(data=message_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FetchMessages(APIView):
    def post(self, request, *args, **kwargs):
        conversation = request.data.get('conversation')

        messages = Message.objects.filter(conversation=conversation)
        data = MessageSerializer(messages, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ScheduleMessageViewSet(ModelViewSet):
    serializer_class = ScheduleMessageSerializer
    queryset = ScheduleMessage.objects.all()

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['sender'] = request.user.id
        request_data['content'] = request.data.get('message')
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        content = serializer.validated_data['content']
        schedule_time = serializer.validated_data['schedule_time']
        schedule_message = serializer.save()

        # scheduling message
        send_scheduled_message.apply_async(args=[schedule_time, schedule_message.id])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RecurrentMessageViewSet(ModelViewSet):
    serializer_class = RecurrentMessageSerializer
    queryset = RecurrentMessage.objects.all()

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        request_data['sender'] = request.user.id
        request_data['content'] = request.data.get('message')
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        recurrent_message = serializer.save()

        every = serializer.validated_data['every']
        period = serializer.validated_data['period']

        schedule, created = IntervalSchedule.objects.get_or_create(every=every, period=period)
        PeriodicTask.objects.create(
            interval=schedule, name='test task', task='chat.tasks.recurrent_messge_task', args=f"[{recurrent_message.id}]"
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ForwardMessageView(APIView):
    def post(self, request, *args, **kwargs):
        message_id = request.data.get('message', None)
        recipients = request.data.get('recipients', [])

        message = Message.objects.filter(id=message_id).first()

        if not message:
            data = {"message": "Invalid message id"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        if not recipients:
            data = {"message": "Invalid recipients"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        message_list = []
        for recipient in recipients:
            receiver = User.objects.filter(phone_number=recipient).first()
            conversation = Conversation.objects.annotate(
                num_participants=Count("participants")).filter(
                    num_participants=2, participants__in=[request.user, receiver]
            ).first()

            if not conversation:
                conversation = Conversation.objects.create()
                conversation.participants.add(request.user, receiver)

            message_data = Message(
                content = message.content,
                conversation = conversation,
                sender = request.user,
                is_forwarded = True
            )
            message_list.append(message_data)

        Message.objects.bulk_create(message_list, batch_size=100)
        data = {"message": "Message forwarded successfully"}
        return Response(data, status=status.HTTP_200_OK)
