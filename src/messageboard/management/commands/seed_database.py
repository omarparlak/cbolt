import random

from django.core.management.base import BaseCommand

from messageboard.factories import TopicFactory, ThreadFactory, MessageFactory


class Command(BaseCommand):
    help = "Seed example data into the database."

    def handle(self, *args, **options):
        for i in range(5):
            topic = TopicFactory()

            num_threads = random.randint(10, 50)
            for _ in range(num_threads):
                thread = ThreadFactory(topic=topic)

                num_messages = random.randint(25, 100)
                for _ in range(num_messages):
                    MessageFactory(thread=thread)

        return
