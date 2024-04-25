from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import SendMessageView, FetchConversationView, FetchMessages, ScheduleMessageViewSet, \
                    ForwardMessageView, RecurrentMessageViewSet

router = DefaultRouter()

router.register('schedule_message', ScheduleMessageViewSet, basename='schedule_message')
router.register('recurrent_message', RecurrentMessageViewSet, basename='recurrent_message')

urlpatterns = [
    # path("", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),

    # path('conversation/create/', views.ConversationCreateAPIView.as_view(), name='conversation-create'),
    # path('conversation/<int:conversation_id>/message/', views.MessageListCreateAPIView.as_view(), name='message-list-create'),

    path('fetch_conversation/', FetchConversationView.as_view(), name='fetch_conversation'),
    path('send_message/', SendMessageView.as_view(), name='send_message'),
    path('fetch_messages/', FetchMessages.as_view(), name='fetch_messages'),
    path('forward/', ForwardMessageView.as_view(), name='forward'),
    path('', include(router.urls)),
]
