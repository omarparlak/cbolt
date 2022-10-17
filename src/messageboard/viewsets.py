from rest_framework import viewsets

from messageboard.models import Topic, Thread, Message
from messageboard.serializers import (
    TopicSerializer,
    ThreadSerializer,
    MessageSerializer,
)


class TopicViewSet(viewsets.ModelViewSet):
    """
    Django REST Framework Viewset for Topics.

    Analogous to Django Views. Essentially exposes the TopicSerializer as a
    JSON payload.

    https://www.django-rest-framework.org/api-guide/viewsets/

    Args:
        viewsets.ModelViewSet: Base Django REST Framework ModelViewSet class.
    """

    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


class ThreadViewSet(viewsets.ModelViewSet):
    """
    Django REST Framework Viewset for Threads.

    Analogous to Django Views. Essentially exposes the ThreadSerializer as a
    JSON payload.

    https://www.django-rest-framework.org/api-guide/viewsets/

    Args:
        viewsets.ModelViewSet: Base Django REST Framework ModelViewSet class.
    """

    serializer_class = ThreadSerializer
    queryset = Thread.objects.all()


class MessageViewSet(viewsets.ModelViewSet):
    """
    Django REST Framework Viewset for Messages.

    Analogous to Django Views. Essentially exposes the MessageSerializer as a
    JSON payload.

    https://www.django-rest-framework.org/api-guide/viewsets/

    Args:
        viewsets.ModelViewSet: Base Django REST Framework ModelViewSet class.
    """

    serializer_class = MessageSerializer
    queryset = Message.objects.all()
