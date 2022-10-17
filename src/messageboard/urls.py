from django.conf.urls import include, url
from django.urls import path

from rest_framework import routers

from messageboard.views import (
    AddMessageView,
    AddThreadView,
    ListMessagesView,
    ListThreadsView,
    ListTopicsView,
)
from messageboard.viewsets import MessageViewSet, ThreadViewSet, TopicViewSet


router = routers.DefaultRouter()
router.register(r"topics", TopicViewSet)
router.register(r"threads", ThreadViewSet)
router.register(r"messages", MessageViewSet)

urlpatterns = [
    url(r"^$", ListTopicsView.as_view(), name="topics"),
    url(r"^topic/(?P<topic_slug>[\w\-]+)/$", ListThreadsView.as_view(), name="threads"),
    url(
        r"^topic/(?P<topic_slug>[\w\-]+)/new-thread/$",
        AddThreadView.as_view(),
        name="new_thread",
    ),
    url(
        r"^topic/(?P<topic_slug>[\w\-]+)/thread/(?P<thread_id>\d+)/$",
        ListMessagesView.as_view(),
        name="messages",
    ),
    url(
        r"^topic/(?P<topic_slug>[\w\-]+)/thread/(?P<thread_id>\d+)/new-message/$",
        AddMessageView.as_view(),
        name="new_message",
    ),
    path("api/", include(router.urls)),
]
