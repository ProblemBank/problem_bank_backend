from django.forms.widgets import Select
from django import forms


class MoratabEditor(forms.Textarea):
    template_name = 'https://bankbackend.rastaiha.ir/static/templates/editor/index.html'
