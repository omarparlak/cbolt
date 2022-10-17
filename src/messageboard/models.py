from django.utils import timezone

from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Topic(models.Model):
    """
    Models the outermost data structure in the message board.

    *Topic* > Thread > Message
    """

    title = models.CharField(max_length=64, unique=True)
    slug = models.CharField(max_length=32, unique=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.slug = slugify(self.title)
        self.save()

    def __str__(self):
        return self.slug

    def get_url(self):
        """
        Returns URL for Topic instance
        """
        return reverse("threads", args=[str(self.slug)])

    def create_thread(self, title: str, author_name: str):
        """
        Helper method creates a Thread within this Topic. Automatically sets
        created_date to current date-time.

        Args:
            title (str): Thread title
            author_name (str): Thread author

        Returns:
            Thread
        """
        return Thread.objects.create(
            title=title,
            topic=self,
            author_name=author_name,
            created_date=timezone.now(),
        )

    @property
    def threads(self):
        """
        Helper method returns all Threads within this Topic, ordered in reverse
        chronological order.

        Returns:
            QuerySet[Thread]
        """
        return self.thread_set.all().order_by("-created_date")


class Thread(models.Model):
    """
    Models the middle data structure in the message board.

    Topic > *Thread* > Message
    """

    title = models.CharField(max_length=120, blank=False, unique=True)
    topic = models.ForeignKey(Topic, null=True, blank=False, on_delete=models.SET_NULL)
    author_name = models.CharField(max_length=80, blank=False, null=False)
    created_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title[:32]}"

    def get_url(self):
        """
        Returns URL for Thread instance
        """
        return reverse("messages", args=[str(self.topic.slug), str(self.id)])

    def create_message(self, content: str, author_name: str):
        """
        Helper method creates a Message within this Thread. Automatically sets
        created_date to current date-time.

        Args:
            content (str): Message body
            author_name (str): Message author

        Returns:
            Message
        """
        return Message.objects.create(
            content=content,
            thread=self,
            author_name=author_name,
            created_date=timezone.now(),
        )

    @property
    def messages(self):
        """
        Helper method returns all Messages within this Thread, ordered
        chronologically. Filters out any Messages created _before_ the Thread
        instance.

        Returns:
            QuerySet[Message]
        """
        return self.message_set.filter(created_date__gte=self.created_date).order_by(
            "created_date"
        )


class Message(models.Model):
    """
    Models the innermost data structure in the message board.

    Topic > Thread > *Message*
    """

    content = models.TextField()
    thread = models.ForeignKey(
        Thread, null=True, blank=False, on_delete=models.SET_NULL
    )
    author_name = models.CharField(max_length=80, blank=False, null=False)
    created_date = models.DateTimeField()

    def __str__(self):
        return f"{self.content[:32]}"

    @property
    def topic(self):
        """
        Helper method returns the Topic a message is associated with.

        Returns:
            Topic
        """
        return self.thread.topic
