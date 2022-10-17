from datetime import timezone
import factory

from messageboard.models import Topic, Thread, Message


class TopicFactory(factory.Factory):
    """
    Factory for producing sane Topic objects.

    https://factoryboy.readthedocs.io/en/latest/reference.html#factory.Factory

    Args:
        factory.Factory: Base Factory class.
    """

    class Meta:
        """
        Declare that we are building a factory around the Topic class.
        """

        model = Topic

    # We define Titles to be 3 words sentences.
    title = factory.Faker("sentence", nb_words=3, variable_nb_words=True)


class ThreadFactory(factory.Factory):
    """
    Factory for producing sane Thread objects.

    https://factoryboy.readthedocs.io/en/latest/reference.html#factory.Factory

    Args:
        factory.Factory: Base Factory class.
    """

    class Meta:
        """
        Declare that we are building a factory around the Thread class.
        """

        model = Thread

    # Titles are sentences, approximately 8 words in length
    title = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    # Author Names are auto-generated usernames
    author_name = factory.Faker("user_name")
    # Created dates are randomly distributed over the last year
    created_date = factory.Faker(
        "date_time_between", start_date="-2y", end_date="-1y", tzinfo=timezone.utc
    )

    @factory.post_generation
    def topic(self, create, extracted, **kwargs):
        """
        Thread topics are generated as the last creation hook.

        https://factoryboy.readthedocs.io/en/latest/reference.html#postgeneration

        Args:
            create (bool): Which strategy was used.
            extracted (Optional[Topic]): None unless value was passed in for
                PostGeneration declaration.
        """
        if not create or not extracted:
            return

        self.topic = extracted
        self.save()


class MessageFactory(factory.Factory):
    """
    Factory for producing sane Message objects.

    https://factoryboy.readthedocs.io/en/latest/reference.html#factory.Factory

    Args:
        factory.Factory: Base Factory class.
    """

    class Meta:
        """
        Declare that we are building a factory around the Message class.
        """

        model = Message

    # Paragraph, approximately 3 sentences in length
    content = factory.Faker("paragraph", nb_sentences=3, variable_nb_sentences=True)
    # Author Names are auto-generated usernames
    author_name = factory.Faker("user_name")
    # Created dates are randomly distributed over the last year
    created_date = factory.Faker(
        "date_time_between", start_date="-1y", end_date="now", tzinfo=timezone.utc
    )

    @factory.post_generation
    def thread(self, create, extracted, **kwargs):
        """
        Message threads are generated as the last creation hook.

        https://factoryboy.readthedocs.io/en/latest/reference.html#postgeneration

        Args:
            create (bool): Which strategy was used.
            extracted (Optional[Thread]): None unless value was passed in for
                PostGeneration declaration.
        """
        if not create or not extracted:
            return

        self.thread = extracted
        self.save()
