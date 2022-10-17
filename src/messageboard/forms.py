from django import forms

from messageboard.models import Thread, Message

# NOTE: We do not have an AddTopicForm.


class AddThreadForm(forms.ModelForm):
    """
    Form to add a Thread to a Topic.

    Args:
        forms.ModelForm: Base Django ModelForm class. Auto-generates a form
            based on a model and exposed fields.
        https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/

    Returns:
        AddThreadForm.
    """

    class Meta:
        """
        Inherits from the Thread model.

        Exposes the Title and Author Name fields for use input.
        """

        model = Thread
        fields = ("title", "author_name")

    def __init__(self, *args, **kwargs):
        """
        Set the Thread's Topic.
        """
        self.topic = kwargs.pop("topic")

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Save the Thread in the desired Topic.

        Returns:
            Thread: The newly created Thread.
        """
        return self.topic.create_thread(
            title=self.cleaned_data["title"],
            author_name=self.cleaned_data["author_name"],
        )


class AddMessageForm(forms.ModelForm):
    """
    Form to add a new Message to a Thread.

    Args:
        forms.ModelForm: Base Django ModelForm class. Auto-generates a form
            based on a model and exposed fields.
        https://docs.djangoproject.com/en/2.2/topics/forms/modelforms/

    Returns:
        AddMessageForm.
    """

    class Meta:
        """
        Inherits from the Message class.

        Exposes the Content and Author Name fields for user input.
        """

        model = Message
        fields = ("content", "author_name")

    def __init__(self, *args, **kwargs):
        """
        Set the Message's Thread.
        """
        self.thread = kwargs.pop("thread")

        super().__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        Saves the Message submitted in the Form to the Thread.

        Returns:
            Message: The Message submitted in the AddMessageForm.
        """
        return self.thread.create_message(
            content=self.cleaned_data["content"],
            author_name=self.cleaned_data["author_name"],
        )
