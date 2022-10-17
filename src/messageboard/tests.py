import random

from django.db.utils import IntegrityError
from django.test import TestCase

from messageboard.factories import ThreadFactory, TopicFactory
from messageboard.models import Thread, Topic


class TopicTestCases(TestCase):
    """
    Automated Tests for Topics.

    Focuses mostly on testing the Topic model.

    Args:
        TestCase: Base TestCase class. Documented well on this page:
        https://docs.djangoproject.com/en/2.2/topics/testing/overview/
    """

    def test_topic_slugs(self):
        """
        'Topic.slug' is a slugified versions of 'Topic.title'.
        """
        given_title = "Python 3 > Python 2!!!"
        expected_slug = "python-3-python-2"

        generated_topic = TopicFactory(title=given_title)

        self.assertTrue(isinstance(generated_topic, Topic))
        self.assertEqual(expected_slug, generated_topic.slug)

    def test_duplicate_topics(self):
        """
        Topics titles must be unique.
        """
        generated_topic = TopicFactory()

        # Creating a new topic with the same title should raise an error
        with self.assertRaises(IntegrityError):
            _ = TopicFactory(title=generated_topic.title)

    def test_topic_with_threads(self):
        """
        Topics create Threads with the the 'create_thread' method.
        Topics have a list of threads.
        """
        # Generate a topic
        topic = TopicFactory()

        # Generate 5 threads in that topic
        threads = [
            topic.create_thread(title=f"{i}{i}{i}", author_name=f"{i}{i}")
            for i in range(5)
        ]

        # There should be five threads
        all_threads = Thread.objects.all()
        self.assertEqual(len(all_threads), 5)
        for thread in threads:
            # Each topic should be in the list we generated above
            self.assertIn(thread, all_threads)
            # That thread's topic should be the only topic generated
            self.assertEqual(thread.topic, topic)

        # We cannot compare these two querysets directly
        # So we zip the two Lists and compare elements one by one
        all_topics_sorted = Thread.objects.filter(topic=topic).order_by("-created_date")
        for (a, b) in zip(topic.threads, all_topics_sorted):
            self.assertEqual(a, b)

    def test_topic_url(self):
        """
        Topic URLs should be of the Form
            /topic/{topic_slug}/
        """
        topic = TopicFactory()

        expected_url = f"/topic/{topic.slug}/"
        actual_url = topic.get_url()

        self.assertEqual(expected_url, actual_url)


class ThreadTestCases(TestCase):
    """
    Automated Tests for Threads.

    Focuses mostly on testing the Thread model.

    Args:
        TestCase: Base TestCase class. Documented well on this page:
        https://docs.djangoproject.com/en/2.2/topics/testing/overview/
    """

    def setUp(self):
        """
        Setup a Topic to add Threads to.
        """
        self.topic = TopicFactory()

    def test_thread_url(self):
        """
        Thread URLs follow the form:
            /topic/{topic_slug}/thread/{thread_id}/
        """
        thread = ThreadFactory(topic=self.topic)

        expected_url = f"/topic/{self.topic.slug}/thread/{thread.id}/"
        actual_url = thread.get_url()

        self.assertEqual(expected_url, actual_url)

    def test_topic_nulls_thread(self):
        """
        Threads may be deleted from Topics.
        """
        temp_thread = ThreadFactory(topic=self.topic)
        temp_thread.delete()

        self.topic.refresh_from_db()
        self.assertEqual(len(self.topic.threads), 0)

    def test_topic_title_unique(self):
        """
        Topics must have a unique title.
        """
        thread_a = ThreadFactory(topic=self.topic)
        with self.assertRaises(IntegrityError):
            _ = ThreadFactory(topic=self.topic, title=thread_a.title)

    def test_create_message(self):
        """
        Threads have a 'create_message' method that spawns a new Message and
        adds it to that Thread.
        """
        thread = ThreadFactory(topic=self.topic)

        message = thread.create_message(
            content=str(random.randrange(100, 1000)),
            author_name=str(random.randrange(0, 99)),
        )

        self.assertEqual(len(thread.messages), 1)
        self.assertIn(message, thread.messages)

    def test_get_thread_messages(self):
        """
        Threads have a list of Messages.
        """
        thread = ThreadFactory(topic=self.topic)

        messages = [
            thread.create_message(content=f"{i}{i}{i}", author_name=f"{i}{i}")
            for i in range(5)
        ]

        for message in messages:
            self.assertIn(message, thread.messages)
            self.assertEqual(message.thread, thread)

    def test_thread_required_fields(self):
        """
        Threads require the 'author_name' and 'title' fields.
        """
        with self.assertRaisesMessage(
            TypeError,
            "create_thread() missing 1 required positional argument: 'author_name'",
        ):
            _ = self.topic.create_thread(title="Foo")

        with self.assertRaisesMessage(
            TypeError, "create_thread() missing 1 required positional argument: 'title'"
        ):
            _ = self.topic.create_thread(author_name="Foo B. Baz")

        with self.assertRaisesMessage(
            TypeError,
            "create_thread() missing 2 required positional arguments: 'title' and 'author_name'",
        ):
            _ = self.topic.create_thread()


class MessageTestCases(TestCase):
    """
    Automated Tests for Messages.

    Focuses mostly on testing the Messages model.

    Args:
        TestCase: Base TestCase class. Documented well on this page:
        https://docs.djangoproject.com/en/2.2/topics/testing/overview/
    """

    def setUp(self):
        """
        Use the Factory's to create a Topic and Thread to add Messages to.
        """
        self.topic = TopicFactory()
        self.thread = ThreadFactory(topic=self.topic)

    def test_get_messages_thread(self):
        """
        A Message has a relationship to it's Thread.
        """
        message = self.thread.create_message(content="Foo", author_name="Foo B. Baz")

        self.assertEqual(message.thread, self.thread)

    def test_message_required_fields(self):
        """
        A Message requires both the 'author_name' and 'content' fields.
        """
        with self.assertRaisesMessage(
            TypeError,
            "create_message() missing 1 required positional argument: 'content'",
        ):
            _ = self.thread.create_message(author_name="Foo B. Baz")

        with self.assertRaisesMessage(
            TypeError,
            "create_message() missing 1 required positional argument: 'author_name'",
        ):
            _ = self.thread.create_message(content="Foo")

        with self.assertRaisesMessage(
            TypeError,
            "create_message() missing 2 required positional arguments: 'content' and 'author_name'",
        ):
            _ = self.thread.create_message()
