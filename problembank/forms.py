from django import forms
from .widgets import MoratabEditor
from .models import Account, Hardness

class QuestionForm(forms.ModelForm):

    text = forms.CharField(widget=MoratabEditor)
    answer = forms.CharField(widget=MoratabEditor, required=False)
    
