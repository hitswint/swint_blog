from django import forms
from django_comments.forms import CommentForm, COMMENT_MAX_LENGTH
from django.utils.translation import pgettext_lazy, ungettext, ugettext, ugettext_lazy as _
from django_summernote.widgets import SummernoteWidget


class CommentFormCustomized(CommentForm):
    comment = forms.CharField(
        label=_('Comment'),
        widget=SummernoteWidget(),
        max_length=COMMENT_MAX_LENGTH)
