from django.http import HttpResponseRedirect
from django.views import View
from django.shortcuts import render, get_object_or_404

from messageboard.forms import AddThreadForm, AddMessageForm
from messageboard.models import Topic, Thread


class ListTopicsView(View):
    """
    Displays all Topics in the message board.

    Django Class-based views docs:
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/
    """

    def get(self, request):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP GET request.

        Returns:
            django.http.response.HttpResponse: Rendered List of Topics.
        """
        topics = Topic.objects.all()
        return render(request, "messageboard/topics.html", {"topics": topics})


class ListThreadsView(View):
    """
    Displays all Threads for a given Topic.

    Django Class-based views docs:
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/
    """

    def get(self, request, topic_slug):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP GET request.
            topic_slug (str): Slug for Topic to list the Threads of.

        Returns:
            django.http.response.HttpResponse: Rendered list of Threads.
        """
        topic = get_object_or_404(Topic, slug=topic_slug)
        threads = topic.threads
        return render(
            request, "messageboard/threads.html", {"topic": topic, "threads": threads}
        )


class AddThreadView(View):
    """
    Add a Thread to a given Topic.

    Django Class-based views docs:
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/
    """

    form_class = AddThreadForm
    template_name = "messageboard/new_thread.html"

    def get(self, request, topic_slug):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP GET request.
            topic_slug (str): Slug for Topic to add a Thread to.

        Returns:
            HttpResponse: New Topic form.
        """
        topic = self.configure(request, topic_slug)
        form = self.form_class(topic=topic)

        return self.common_context(request, form, topic)

    def post(self, request, topic_slug):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP POST request.
            topic_slug (str): Slug for Topic to add a Thread to.

        Returns: Either[HttpResponseRedirect|HttpResponse]
            HttpResponseRedirect: Redirect to the created Topic.
            HttpResponse: The New Topic form.
        """
        topic = self.configure(request, topic_slug)
        form = self.form_class(request.POST, topic=topic)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(topic.get_url())
        else:
            return self.common_context(request, form, topic)

    def configure(self, request, topic_slug):
        """
        Returns the Topic with the given Slug, or a 404 if the Topic is not found.

        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            topic_slug (str): Slug for Topic to add a Thread to.

        Returns:
            messageboard.models.Topic: The Topic object with the given slug.
        """
        topic = get_object_or_404(Topic, slug=topic_slug)
        return topic

    def common_context(self, request, form, topic):
        """
        Returns the New Topic Django Form.

        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            form (messageboard.forms.AddThreadForm): Form for creating a new Thread.
            topic (messageboard.models.Topic): Topic Model object.

        Returns:
            django.http.response.HttpResponse: Rendered Topic.
        """
        return render(request, self.template_name, {"form": form, "topic": topic})


class ListMessagesView(View):
    """
    Displays all Messages for a given Thread.

    Django Class-based views docs:
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/
    """

    def get(self, request, topic_slug, thread_id):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            topic_slug (str): Topic slug containing Topic to add message to.
            thread_id (str(int)): Thread ID to add message to.

        Returns:
            django.http.response.HttpResponse: Rendered List of Messages.
        """
        thread = get_object_or_404(Thread, pk=thread_id)
        messages = thread.messages
        return render(
            request,
            "messageboard/messages.html",
            {"thread": thread, "messages": messages},
        )


class AddMessageView(View):
    """
    Add a Message to a given Thread.

    Django Class-based views docs:
    https://docs.djangoproject.com/en/2.2/topics/class-based-views/
    """

    form_class = AddMessageForm
    template_name = "messageboard/new_message.html"

    def get(self, request, topic_slug, thread_id):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            topic_slug (str): Slug for Topic to add message to.
            thread_id (str(int)): ID of Thread to add message to.

        Returns:
            HttpResponse: New Message form.
        """
        thread = self.configure(request, topic_slug, thread_id)
        form = self.form_class(thread=thread)

        return self.common_context(request, form, thread)

    def post(self, request, topic_slug, thread_id):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            topic_slug (str): Topic slug containing Topic to add message to.
            thread_id (str(int)): Thread ID to add message to.

        Returns: Either[HttpResponseRedirect|HttpResponse]
            HttpResponseRedirect: Redirect to the created Topic.
            HttpResponse: The New Topic form.
        """
        thread = self.configure(request, topic_slug, thread_id)
        form = self.form_class(request.POST, thread=thread)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(thread.get_url())
        else:
            return self.common_context(request, form, thread)

    def configure(self, request, topic_slug, thread_id):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            topic_slug (str): Topic slug containing Topic to add message to.
            thread_id (str(int)): Thread ID to add message to.

        Returns:
            messageboard.models.Message: Specified Thread or a 404.
        """
        thread = get_object_or_404(Thread, pk=thread_id)
        return thread

    def common_context(self, request, form, thread):
        """
        Args:
            request (django.core.handlers.wsgi.WSGIRequest): Incoming HTTP request.
            form (messageboard.forms.AddMessageForm): [description]
            thread (messageboard.models.Thread): [description]

        Returns:
            django.http.response.HttpResponse: Rendered Message.
        """
        return render(request, self.template_name, {"form": form, "thread": thread})
