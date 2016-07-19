"""Module with forms declarations"""
from django import forms


class SubmissionForm(forms.Form):
    """New submission Form."""
    task_file = forms.FileField(
        label='Select a File',
        help_text='max. 42 Megabytes'
    )
    task_description = forms.CharField(
        label='Description:',
        max_length=1000,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '(optional)'})
        )
