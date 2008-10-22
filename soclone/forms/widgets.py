from django import forms
from django.utils.safestring import mark_safe

class MarkdownTextArea(forms.Textarea):
    """
    A ``<textarea>`` which includes JavaScript media for the `Wysiwym
    Markdown editor`_.

    .. _Wysiwym Markdown editor: http://code.google.com/p/wmd/
    """
    class Media:
        js = ('js/wmd/wmd.js',)
